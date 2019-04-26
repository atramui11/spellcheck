/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

// NOTE: new type added here
const bit<16> TYPE_MYTUNNEL = 0x1212;
const bit<16> TYPE_IPV4 = 0x800;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}


header ipv4_t {
    bit<4>    version;
    bit<4>    ihl;
    bit<8>    diffserv;
    bit<16>   totalLen;
    bit<16>   identification;
    bit<3>    flags;
    bit<13>   fragOffset;
    bit<8>    ttl;
    bit<8>    protocol;
    bit<16>   hdrChecksum;
    ip4Addr_t srcAddr;
    ip4Addr_t dstAddr;
}

header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<3>  res;
    bit<3>  ecn;
    bit<6>  ctrl;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}


header spchk1_t { bit<8> word; bit<8> rsp; }
header spchk2_t { bit<16> word; bit<8> rsp; }
header spchk3_t { bit<24> word; bit<8> rsp; }
header spchk4_t { bit<32> word; bit<8> rsp; }


//represents a uniform header
header_union spellCheck_t {
    spchk1_t spchk1;
    spchk2_t spchk2;
    spchk3_t spchk3;
    spchk4_t spchk4;
}

struct metadata {/* empty */}

struct headers {
    ethernet_t   ethernet;
    ipv4_t       ipv4;
    tcp_t        tcp;
    spellCheck_t spchk;

}

/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    
    state start {
        packet.extract(hdr.ethernet);
        packet.extract(hdr.ipv4);
        packet.extract(hdr.tcp);
        
        /*        
        transition select(hdr.spchk.wordLength) {
            (true, false, false, false): parse1Byte;
            (false, true, false, false): parse2Bytes;
            (false, false, true, false): parse3Bytes;
            (false, false, false, true): parse4Bytes;
        }
        */

        //transition parse4Bytes;
        transition parse3Bytes;

        

        //packet.extract(hdr.spchk);
        //transition accept;
    }

    state parse1Byte {
        packet.extract(hdr.spchk.spchk1);
        transition accept;
    }

    state parse2Bytes {
        packet.extract(hdr.spchk.spchk2);
        transition accept;
    }

    state parse3Bytes {
        packet.extract(hdr.spchk.spchk3);
        transition accept;
    }

    state parse4Bytes {
        packet.extract(hdr.spchk.spchk4);
        transition accept;
    }


}

/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {


    action drop() {mark_to_drop();}
    action pkt_fwd(egressSpec_t dport) {standard_metadata.egress_spec = dport;}


    //default action. if executed means no match in a wordDict table
    action defaultFail() {hdr.spchk.spchk4.rsp = 0;}


  
    action installWordEntry1(bit<8> resp) {hdr.spchk.spchk1.rsp = resp;}
    action installWordEntry2(bit<8> resp) {hdr.spchk.spchk2.rsp = resp;}
    action installWordEntry3(bit<8> resp) {hdr.spchk.spchk3.rsp = resp;}
    action installWordEntry4(bit<8> resp) {hdr.spchk.spchk4.rsp = resp;}




    table wordDict1 {
        key = {hdr.spchk.spchk1.word : exact;}
        actions = {installWordEntry1; defaultFail; drop;NoAction;}
        size=1024;
        default_action = NoAction; 
    }

    table wordDict2 {
        key = {hdr.spchk.spchk2.word : exact;}
        actions = {installWordEntry2; defaultFail; drop;NoAction;}
        size=1024;
        default_action = NoAction; 
    }

    table wordDict3 {
        key = {hdr.spchk.spchk3.word : exact;}
        actions = {installWordEntry3; defaultFail; drop;NoAction;}
        size=1024;
        default_action = NoAction; 
    }

    table wordDict4 {
        key = {hdr.spchk.spchk4.word : exact;}
        actions = {installWordEntry4; defaultFail; drop;NoAction;}
        size=1024;
        default_action = defaultFail(); //failed to find match
    }

   
    table packetForward {
        key = {
            hdr.tcp.srcPort: exact;
        }
        actions = {
            pkt_fwd;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = drop();
    }



    
    apply {
        packetForward.apply();
        wordDict1.apply();
        wordDict2.apply();
        wordDict3.apply();
        wordDict4.apply();
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers  hdr, inout metadata meta) {
     apply {
	update_checksum(
	    hdr.ipv4.isValid(),
            { hdr.ipv4.version,
	      hdr.ipv4.ihl,
              hdr.ipv4.diffserv,
              hdr.ipv4.totalLen,
              hdr.ipv4.identification,
              hdr.ipv4.flags,
              hdr.ipv4.fragOffset,
              hdr.ipv4.ttl,
              hdr.ipv4.protocol,
              hdr.ipv4.srcAddr,
              hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);
    }
}

/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.spchk);
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;