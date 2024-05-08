"""
@Project :SIL_data_annotation_tool_error_statistic_v4.1.py
@File    :cpp_code.py
@IDE     :PyCharm
@Author  :wlf
@Date    :4/17/24 4:33 PM
"""


def generate_code(struct_name, member_structs, array_size):
    code = ""

    # Generate compareStructs function
    code += f"bool compareStructs(const {struct_name}& dict1, const {struct_name}& dict2, uint32_t& sequence, size_t acc) {{\n"
    code += f"    float acc_parm = 1;\n"
    code += f"    while (acc-- > 0){{\n"
    code += f"        acc_parm *= 1e1;\n"
    code += f"    }}\n"
    for struct_idx, (member_name, member_list) in enumerate(member_structs.items(), start=1):
        if struct_idx == 1:
            for var_type, var_name in member_structs[member_name]:
                if var_type.startswith('h_f'):
                    # float b = (int)a + (int)((a - int(a)) * 1e3) / 1e3;
                    new_var_type = var_type.replace('h_f', 'h_s')
                    code += f"    {var_type} dict1_var = ({new_var_type})dict1.{var_name} + ({new_var_type})((dict1.{var_name} - ({new_var_type})dict1.{var_name}) * acc_parm) / acc_parm;\n"
                    code += f"    {var_type} dict2_var = ({new_var_type})dict2.{var_name} + ({new_var_type})((dict2.{var_name} - ({new_var_type})dict2.{var_name}) * acc_parm) / acc_parm;\n"
                    code += f"    if (dict1_var != dict2_var) {{\n"
                else:
                    code += f"    if (dict1.{var_name} != dict2.{var_name}) {{\n"
                code += f"        std::cout << \"{member_name}: \" << \"{var_name}\" << \" is different, seq:\" << sequence\n" \
                        f"        << \", they are: \" << dict1.{var_name} << \" and \" << dict2.{var_name} << std::endl;\n"
                code += "         return false;\n"
                code += "    }\n"
        else:
            code += f"    for (size_t i = 0; i < {array_size}; ++i) {{\n"
            for var_type, var_name in member_structs[member_name]:
                if var_type.startswith('h_f'):
                    new_var_type = var_type.replace('h_f', 'h_s')
                    code += f"        {var_type} dict1_var = ({new_var_type})dict1.data_list[i].{var_name} + ({new_var_type})((dict1.data_list[i].{var_name} - ({new_var_type})dict1.data_list[i].{var_name}) * acc_parm) / acc_parm;\n"
                    code += f"        {var_type} dict2_var = ({new_var_type})dict2.data_list[i].{var_name} + ({new_var_type})((dict2.data_list[i].{var_name} - ({new_var_type})dict2.data_list[i].{var_name}) * acc_parm) / acc_parm;\n"
                    code += f"        if (dict1_var != dict2_var) {{\n"
                else:
                    code += f"        if (dict1.data_list[i].{var_name} != dict2.data_list[i].{var_name}) {{\n"
                code += f"            std::cout << \"{member_name}: \" << \"data_list[i].{var_name}\" << \" is different, seq:\" << sequence\n" \
                        f"            << \", they are: \" << dict1.data_list[i].{var_name} << \" and \" << dict2.data_list[i].{var_name} << std::endl;\n"
                code += "            return false;\n"
                code += "        }\n"
            code += "    }\n"

    code += "    return true;\n"
    code += "}\n\n"

    # # Generate compareArrays function
    # code += f"    for (size_t i = 0; i < size; ++i) {{\n"
    # code += f"        if (!compareStructs(array1[i], array2[i])) {{\n"
    # code += f"            std::cout << \"Difference found at index \" << i << std::endl;\n"
    # code += f"        }}\n"
    # code += "    }\n"
    # code += "}\n\n"

    return code


# Example usage
# struct_name = "BIN_REFLECTOR_DICT"
# array_size = "REFLECTOR_MAX_NUM"
# member_structs = {
#     struct_name: [
#         # ("REFLECTOR", "data_list[REFLECTOR_MAX_NUM]"),
#         ("h_s16", "max_num"),
#         ("h_s16", "valid_num")
#     ],
#     "REFLECTOR": [
#         ("h_f32", "vy"),
#         ("h_f32", "speed"),
#         ("h_f32", "speed_compensation"),
#         ("h_f32", "speed_res"),
#         ("h_f32", "ry"),
#         ("h_f32", "rx"),
#         ("h_f32", "vx"),
#         ("h_f32", "range"),
#         ("h_f32", "angle"),
#         ("h_f32", "angle_rcs"),
#         ("h_s16", "range_bin"),
#         ("h_s16", "dop_bin"),
#         ("h_f32", "power"),
#         ("h_f32", "az_snr"),
#         ("h_f32", "noise"),
#         ("h_f32", "guardrail_score"),
#         ("h_s8", "tgt2_pre_id"),
#         ("union { h_u32 flg_all; FLAGS_REFLECTOR flags; }", "FLAGS.flg_all")
#     ]
# }

# struct_name = "BIN_TARGET2_DICT"
# array_size = "TARGET2_MAX_NUM"
# member_structs = {
#     struct_name: [
#         # ("REFLECTOR", "data_list[REFLECTOR_MAX_NUM]"),
#         ("h_s16", "max_num"),
#         ("h_s16", "valid_num")
#     ],
#     "TARGET2": [
#         ("h_f32", "vy"),
#         ("h_f32", "ry"),
#         ("h_f32", "rx"),
#         ("h_f32", "ry_next"),
#         ("h_f32", "rx_next"),
#         ("h_f32", "vy_next"),
#         ("h_f32", "vx_next"),
#         ("h_f32", "rx_pre"),
#         ("h_f32", "init_rx"),
#         ("h_f32", "init_ry"),
#         ("h_s8", "max_score_direction"),
#         ("h_s8", "init_v_stable_score"),
#         ("h_s8", "tgt2_v_reverse"),
#         ("h_s8", "tgt2_rcta_reserve"),
#         ("h_f32", "vx"),
#         ("h_f32", "range"),
#         ("h_f32", "angle"),
#         ("h_f32", "velocity"),
#         ("h_s16", "dop_bin"),
#         ("h_s16", "range_bin"),
#         ("h_f32", "power"),
#         ("h_s16", "detected_cnt"),
#         ("h_s16", "reflector_id"),
#         ("h_s8", "lost_cnt"),
#         ("h_s8", "delay_creat_tgt3"),
#         ("h_s8", "pre_tgt2_id"),
#         ("h_s8", "cur_tgt2_id"),
#         ("h_f32", "vy_ground"),
#         ("h_f32", "rx_curve"),
#         ("h_s16", "tgt2_score"),
#         ("h_s16", "prob"),
#         ("h_s16", "selflane_prob"),
#         ("h_s16", "in_range_Point_num"),
#         ("h_f32", "assoc_t"),
#         ("h_u32", "glb_tgt2_id"),
#         ("h_f32", "near_ref_var"),
#         ("h_f32", "merged_dy_min"),
#         ("h_f32", "merged_dy_max"),
#         ("h_f32", "merged_dx_min"),
#         ("h_f32", "merged_dx_max"),
#         ("h_f32", "FLAGS.flg_all"),
#     ]
# }

# struct_name = "BIN_TARGET3_DICT"
# array_size = "TARGET3_MAX_NUM"
# member_structs = {
#     struct_name: [
#         # ("REFLECTOR", "data_list[REFLECTOR_MAX_NUM]"),
#         ("h_s16", "max_num"),
#         ("h_s16", "valid_num")
#     ],
#     "TARGET3": [
#         ("h_f32", "ry"),
#         ("h_f32", "vy"),
#         ("h_f32", "ay"),
#         ("h_f32", "rx"),
#         ("h_f32", "vx"),
#         ("h_f32", "ax"),
#         ("h_f32", "ry_ini"),
#         ("h_f32", "rx_ini"),
#         ("h_f32", "ry_next"),
#         ("h_f32", "vy_next"),
#         ("h_f32", "ay_next"),
#         ("h_f32", "rx_next"),
#         ("h_f32", "rx_pre"),
#         ("h_f32", "vx_next"),
#         ("h_f32", "ax_next"),
#         ("h_f32", "angle"),
#         ("h_f32", "range"),
#         ("h_f32", "velocity"),
#         ("h_f32", "power"),
#         ("h_f32", "vy_ground"),
#         ("h_f32", "rx_curve"),
#         ("h_f32", "heading"),
#         ("h_s8", "lost_cnt"),
#         ("h_s8", "pre_tgt3_id"),
#         ("h_s8", "cur_tgt3_id"),
#         ("h_s8", "cur_seg_id"),
#         ("h_s32", "max_associate_cnt_as_truck"),
#         ("h_s16", "dop_bin"),
#         ("h_s16", "range_bin"),
#         ("h_s16", "detected_cnt"),
#         ("h_s16", "reflector_id"),
#         ("h_s16", "prob"),
#         ("h_s16", "selflane_prob"),
#         ("h_s16", "near_car_cnt"),
#         ("h_u16", "associate_cnt_as_truck"),
#         ("h_s16", "obj_class"),
#         ("h_s16", "rcs"),
#         ("h_s16", "max_rcs"),
#         ("h_f32", "width"),
#         ("h_f32", "length"),
#         ("h_f32", "assoc_t"),
#         ("h_u32", "glb_tgt3_id"),
#     ]
# }


# struct_name = "BIN_SEGMENT_DICT"
# array_size = "SEGMENT_MAX_NUM"
# member_structs = {
#     struct_name: [
#         # ("REFLECTOR", "data_list[REFLECTOR_MAX_NUM]"),
#         ("h_s16", "max_num"),
#         ("h_s16", "valid_num"),
#         ("h_s16", "adjacent_num")
#     ],
#     "SEGMENT": [
#         ("h_f32", "ry"),
#         ("h_f32", "vy"),
#         ("h_f32", "ay"),
#         ("h_f32", "rx"),
#         ("h_f32", "vx"),
#         ("h_f32", "ax"),
#         ("h_f32", "doppler"),
#         ("h_s16", "prob"),
#         ("h_s16", "selflane_prob"),
#         ("h_s16", "detected_cnt"),
#         ("h_s8", "cur_tgt3_id"),
#         ("h_s8", "pre_seg_id"),
#         ("h_f32", "vy_ground"),
#         ("h_f32", "rx_curve"),
#         ("h_u32", "glb_seg_id"),
#         ("h_f32", "merged_dy_max"),
#         ("h_f32", "merged_dy_min"),
#         ("h_f32", "merged_dx_min"),
#         ("h_f32", "merged_dx_max"),
#         ("h_f32", "x_l"),
#         ("h_f32", "x_r"),
#         ("h_f32", "length"),
#         ("h_f32", "width"),
#     ]
# }

struct_name = "BIN_TRACK_DICT"
array_size = "TRACK_MAX_NUM"
member_structs = {
    struct_name: [
        # ("REFLECTOR", "data_list[REFLECTOR_MAX_NUM]"),
        ("h_s16", "max_num"),
        ("h_s16", "valid_num"),
        ("h_s16", "FLAGS.flg_all")
    ],
    "TRACK": [
        ("h_f32", "ry"),
        ("h_f32", "vy"),
        ("h_f32", "ay"),
        ("h_f32", "rx"),
        ("h_f32", "vx"),
        ("h_f32", "ax"),
        ("h_f32", "rx_curve"),
        ("h_f32", "vy_ground"),
        ("h_f32", "doppler"),
        ("h_s16", "i16_detected_cnt"),
        ("h_s16", "prob"),
        ("h_s16", "selflane_prob"),
        ("h_s8", "seg_id_cur"),
        ("h_u8", "glb_release_trk_id"),
        ("h_s16", "range_bin_next"),
        ("h_s16", "dop_bin_next"),
        ("h_f32", "merged_dx_min"),
        ("h_f32", "merged_dx_max"),
        ("h_f32", "length"),
        ("h_f32", "width"),
        ("h_u32", "glb_trk_id"),
        ("h_u32", "FLAGS.flg_all"),
    ]
}

cpp_code = generate_code(struct_name, member_structs, array_size)
print(cpp_code)
