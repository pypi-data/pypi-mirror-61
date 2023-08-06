
#include <iostream>

#include "Config.h"
#include "ScalarField.h"
#include "BitfieldField.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>

namespace py = pybind11;

using namespace pybind11;

template<typename T>
void init_scalar(handle& m){
    class_<ScalarField<T>, FieldType>(m, (std::string("Scalar_") + typeid(T).name()).c_str());
}

template<size_t T>
void init_bitfield(handle& m){
    class_<BitfieldField<T>, FieldType>(m, (std::string("BitfieldField") + std::to_string(T*8)).c_str())
        .def_readonly("bit_names", &BitfieldField<T>::bit_names);
}

PYBIND11_MODULE(carconfig, m)
{

    class_<FieldType>(m, "FieldType")
        .def_readwrite("name", &FieldType::name)
        .def_readwrite("data_size", &FieldType::data_size);

    init_scalar<uint8_t>(m);
    init_scalar<int8_t>(m);
    init_scalar<uint16_t>(m);
    init_scalar<int16_t>(m);
    init_scalar<uint32_t>(m);
    init_scalar<int32_t>(m);
    init_scalar<uint64_t>(m);
    init_scalar<int64_t>(m);
    init_scalar<float>(m);
    init_bitfield<1>(m);
    init_bitfield<2>(m);
    init_bitfield<4>(m);

    class_<CANMessageType>(m, "CANMessageType")
        .def_readwrite("id", &CANMessageType::id)
        .def_readwrite("name", &CANMessageType::name)
        .def_readwrite("expected_interval", &CANMessageType::expected_interval)
        .def_readwrite("fields", &CANMessageType::fields)
        .def_readwrite("priority_num", &CANMessageType::priority_num)
        .def_readwrite("publisher", &CANMessageType::publisher);

    class_<Node>(m, "Node")
        .def_readwrite("id", &Node::id)
        .def_readwrite("name", &Node::name)
        .def_readwrite("published", &Node::published)
        .def_readwrite("subscribed", &Node::subscribed);

    class_<Config>(m, "Config")
        .def(init())
        .def("load_from_file", &Config::load_from_file)
        .def_readwrite("message_types_by_id", &Config::message_types_by_id)
        .def_readwrite("message_types_by_name", &Config::message_types_by_name)
        .def_readwrite("message_types", &Config::message_types)
        .def_readwrite("priority_names", &Config::priority_names)
        .def_readwrite("priority_nums_by_name", &Config::priority_nums_by_name)
        .def_readwrite("nodes", &Config::nodes);
}
