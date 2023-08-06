#include "CANMessageType.h"

CANMessageType CANMessageType::UNKNOWN("UNKNOWN");

CANMessageType::CANMessageType(){

}

CANMessageType::CANMessageType(std::string name){
    this->name = name;
}

CANMessageType::~CANMessageType(){
    for(FieldType *field_type : this->fields){
        delete field_type;
    }
}
