/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_MYTUNNEL = 0x1212;
const bit<16> TYPE_IPV4 = 0x800;
const bit<32> MAX_TUNNEL_ID = 1 << 16;


///one letter is 1 byte. to send a word, start with 10 letters
//thats 80 bits for a 10 letter word

typedef bit<9>  egressSpec_t;
typedef bit<9>  ingressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;


header word_to_check_t {
	bit<80> spellcheck_word;
	macAddr_t srcAddr;
	macAddr_t dstAddr;
}


struct metadata { }

struct headers { 
	word_to_check_t    word_to_check;
}



parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start { transition parse_word_to_check; }

	state parse_word_to_check {
		packet.extract(hdr.word_to_check);
		transition accept; //default action, done 
	}



}


control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply { }
}



control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    //this port would be provided by control plane 
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
    apply { }
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
