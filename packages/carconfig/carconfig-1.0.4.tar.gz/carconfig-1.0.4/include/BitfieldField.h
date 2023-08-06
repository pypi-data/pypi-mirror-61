#pragma once

#include <vector>

#include "yaml-cpp/yaml.h"

#include "FieldType.h"

template <size_t S>
class BitfieldField : public FieldType{

    public:

        std::vector<std::string> bit_names;

        BitfieldField(YAML::Node& field_info){
            if(field_info.Type() == YAML::NodeType::Map){
                if(field_info["bits"]){
                    this->bit_names = field_info["bits"].as<std::vector<std::string>>();
                }
            }
            
            this->data_size = S;
        }

        void data_to_string(std::string& dest, uint8_t *data){
            dest = "(bitfield)";
        }

        void data_to_json(json& obj, uint8_t *data){

            for(size_t bit_index = 0; bit_index < bit_names.size(); bit_index++){
                size_t byte_index = bit_index / 8;
                int bit_in_byte = bit_index % 8;
                uint8_t byte = data[byte_index];
                obj[bit_names[bit_index]] = ((byte >> bit_in_byte) & 0x1) == 0x1;
            }
            /*
            int flag_index = 0;
            for(size_t byte_index = 0; byte_index < S; byte_index++){
                uint8_t byte = data[byte_index];
                for(int bit_index = 0; bit_index < 8; bit_index++){
                    obj["a"] = (byte & 0x1) == 0x1;
                    byte = byte >> 1;
                    flag_index++;
                }
            }
            */
        }
};