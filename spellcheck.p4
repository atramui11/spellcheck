/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>


const bit<16> TYPE_IPV4 = 0x800;

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

header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length;
    bit<16> checksum;
}


header spellcheck_t {
	bit<80> spellcheck_word; //80 bits for a 10 letter word
	bit<16> srcPort;
    bit<16> dstPort;
}


struct metadata { }


struct headers { 
    ethernet_t ethernet;
	ipv4_t ipv4; 
	udp_t udp; 
	//spellcheck_t spellcheck; 
}


parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        transition parse_ethernet; 
    }

    
    //state for ethernet header (packets always begin here)
    state parse_ethernet {
    	packet.extract(hdr.ethernet); //problem here!
        transition select (hdr.ethernet.etherType) {
            TYPE_IPV4: parse_ipv4;
            default : accept;
        }

    }

    
    state parse_ipv4 {
   		packet.extract(hdr.ipv4);
    	transition accept;
    }

    /*
    state parse_udp {
    	packet.extract(hdr.udp);
    	transition accept;
    	//transition parse_spellcheck;
    }
    */

    /*
	state parse_spellcheck{
		packet.extract(hdr.spellcheck);
		transition accept;
	}
	*/

}


control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply { }
}


control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action drop() {
        mark_to_drop();
    }
    
    action ipv4_forward(macAddr_t dstAddr, egressSpec_t port) {
        /* TODO: fill out code in action body */
        standard_metadata.egress_spec = port;
        hdr.ethernet.srcAddr = hdr.ethernet.dstAddr;
        hdr.ethernet.dstAddr = dstAddr;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }
    

    //ROUTING TABLE
    table ipv4_lpm {
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            ipv4_forward;
            drop;
            NoAction;
        }
        size = 1024;
        default_action = NoAction();
    }
    
    apply {
        /* TODO: fix ingress control logic
         *  - ipv4_lpm should be applied only when IPv4 header is valid
         */
        ipv4_lpm.apply();
    }








    /*
    apply {
        if (standard_metadata.ingress_port == 401)
            standard_metadata.egress_spec = 500;
        else
            standard_metadata.egress_spec = 1;
    }

    
	action set_egress_spec(bit<9> port) {
		standard_metadata.egress_spec = port;
	}

	table oneHostoneSwitch {
		key = {standard_metadata.ingress_port : exact; }

		actions = {
			set_egress_spec;
			NoAction;
		}
		size = 1024;
		default_action = NoAction();

	}
    

	apply {oneHostoneSwitch.apply();}


	action dictLookup(word_to_check_t, word_to_check) {}

	table word_dict 
	{
	  key = 
	  { hdr.word_to_check.spellcheck_word : lpm; }
	  actions = 
	  {
	    dict_lookup;
	    NoAction;
	  }

	  size = 1024; //would have to be a lot bigger for dictionary table
	  
	  default_action = NoAction();
	}
	*/

}

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

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

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
    	packet.emit(hdr.ethernet); //emit ethernet header into packet
        packet.emit(hdr.ipv4); //emit ipv4 header into packet
    }
}


V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;