#pragma once

#include "FieldType.h"

template <typename T>
class ScalarField : public FieldType{

    public:
        bool big_endian = false;
        double scale = 1.0;

        ScalarField(YAML::Node& field_info){
            this->data_size = sizeof(T);
            if(field_info.Type() == YAML::NodeType::Map && field_info["scale"]){
                this->scale = field_info["scale"].as<double>();
            }
        }

        void data_to_string(std::string& dest, uint8_t *data){
            T *casted = (T*) data;
            dest = std::to_string(*casted);
        }

        void data_to_json(json& obj, uint8_t *data){
            T *casted = (T*) data;

            if(scale == 1.0){
                obj = (*casted);
            }else{
                obj = (*casted) / scale;
            }
            
        }
};