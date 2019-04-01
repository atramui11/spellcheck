/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/******
one letter is 1 byte is 8 bits
to send a word, start with 10 letters
thats 80 bits for a 10 letter word
*******/

header word_to_check_t {
	bit<80> spellcheck_word;
}


struct metadata { }

struct headers { 
	word_to_check_t    word_to_check;
}



parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start { transition accept; }

	//need to update Parser to be able to recognize a word_to_check header within the incoming packets

	state parse_word_to_check {
		packet.extract(hdr.word_to_check);
	}



}





control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply { }
}




control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    apply {
        if (standard_metadata.ingress_port == 1)
            standard_metadata.egress_spec = 2;
        else
            standard_metadata.egress_spec = 1;
    }

    // TODO: declare a new table: word_dictionary
    	//will have to use switch to check spelling in a table as such
    // TODO: Add table entries.
    	//I think through dictionary.json file ?
	
	/*
	table word_dictionary 
	{
	  key = 
	  {
	  	//the key should be the WORD sent in header packet

	    //hdr.ipv4.dstAddr: lpm; //lpm = longest prefix match
	  }


	  actions = 
	  {
	    ipv4_forward;
	    drop;
	    NoAction;
	  }

	  size = 1024; //would have to be a lot bigger for dictionry table
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



V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;
