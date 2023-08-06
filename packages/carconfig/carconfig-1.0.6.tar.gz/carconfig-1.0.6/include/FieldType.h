#pragma once

#include <string>
#include <cstdint>

#include "json.hpp"
#include "yaml-cpp/yaml.h"

using json = nlohmann::json;

class FieldType {

    public:
        static FieldType* create_field_type(std::string& name, YAML::Node& field_info);
        
        std::string name;
        size_t data_size;

        virtual void data_to_string(std::string& string, uint8_t *data);
        virtual void data_to_json(json& obj, uint8_t* data);
        virtual ~FieldType();
};
