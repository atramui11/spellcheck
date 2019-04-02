/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/******
one letter is 1 byte.
to send a word, start w 10 letters
80 bits is a 10 letter word.
*******/


//header for word for spellcheck
header spellcheck_t {
	bit<80> spellcheck_word;
}


struct metadata { }



//add spellcheck word header to struct
struct headers { 
	spellcheck_t    spellcheck;
}



parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

	state start { transition accept; } 

	//this state 
	state parse_word_to_check {
		packet.extract(hdr.word_to_check);
		transition accept;
	}



}





control MyVerifyChecksum(inout headers hdr, inout metadata meta) {   
    apply { }
}




control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {


//simple wire , not sure if appropriate though...
    apply {
        if (standard_metadata.ingress_port == 1)
            standard_metadata.egress_spec = 2;
        else
            standard_metadata.egress_spec = 1;
    }
    
    

    	//will have to use switch to check spelling in a table as such
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


//egress and ingress are where match action tables are  

V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main; //main triggered here
