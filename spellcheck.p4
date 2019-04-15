/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_MYTUNNEL = 0x1212;
const bit<16> TYPE_IPV4 = 0x800;
const bit<32> MAX_TUNNEL_ID = 1 << 16;

typedef bit<9>  egressSpec_t;
typedef bit<9>  ingressSpec_t;
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
    bit<16> length_;
    bit<16> checksum;
}

//header for word for spellcheck. 80 bits for a 10 letter word
header spellcheck_t {
	bit<80> spellcheck_word;
	bit<16> srcPort;
    bit<16> dstPort;
}


struct metadata { }



//add spellcheck word header to struct
struct headers { 
	ethernet_t ethernet;
	ipv4_t ipv4; 
	udp_t udp; 
	spellcheck_t spellcheck; 
}



parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start { 
    	transition parse_ethernet; 
    }

    state parse_ethernet {
    	packet.extract(hdr.ethernet);
    	transition parse_ipv4;
    }


    state parse_ipv4 {
   		packet.extract(hdr.ipv4);
    	transition parse_udp;
    }

    state parse_udp {
    	packet.extract(hdr.udp);
    	transition accept;
    	//transition parse_spellcheck;
    }

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


    //this port provided by control plane 
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


	/*
	action dictLookup(word_to_check_t, word_to_check) {}

	table word_dictionary 
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
     apply { }
}

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
    	//packet.emit(hdr.word_to_check.spellcheck_word)
    }
}


//egress and ingress are where match action tables are  

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main; //main triggered here
