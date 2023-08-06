#include "FieldType.h"

#include <iostream>
#include <string>
#include <cstdint>

#include "ScalarField.h"
#include "BitfieldField.h"

FieldType* FieldType::create_field_type(std::string& name, YAML::Node& field_info){
    std::string type;
    if(field_info.IsScalar()){
        type = field_info.as<std::string>();
    }else{
        type = field_info["type"].as<std::string>();
    }

    FieldType *field = nullptr;

    if(type == "uint8_t"){
        field = new ScalarField<uint8_t>(field_info);
    }else if(type == "int8_t"){
        field = new ScalarField<int8_t>(field_info);
    }else if(type == "uint16_t"){
        field = new ScalarField<uint16_t>(field_info);
    }else if(type == "int16_t"){
        field = new ScalarField<int16_t>(field_info);
    }else if(type == "uint32_t"){
        field = new ScalarField<uint32_t>(field_info);
    }else if(type == "int32_t"){
        field = new ScalarField<int32_t>(field_info);
    }else if(type == "uint64_t"){
        field = new ScalarField<uint64_t>(field_info);
    }else if(type == "int64_t"){
        field = new ScalarField<int64_t>(field_info);
    }else if(type == "float"){
        field = new ScalarField<float>(field_info);
    }else if(type == "bitfield8"){
        field = new BitfieldField<1>(field_info);
    }else if(type == "bitfield16"){
        field = new BitfieldField<2>(field_info);
    }else if(type == "bitfield32"){
        field = new BitfieldField<4>(field_info);
    }
    
    if(field == nullptr){
        std::cout << "Type = " << type << std::endl;
    }else{
        field->name = name;
    }

    
    return field;
}

void FieldType::data_to_string(std::string& dest, uint8_t *data){
    dest = "(not implemented)";
}

void FieldType::data_to_json(json& obj, uint8_t *data){
    obj = "(not implemented)";
}

FieldType::~FieldType(){

}
