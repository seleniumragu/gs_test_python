# -*- coding: utf-8 -*-


class CompareUtils(object):

    @staticmethod
    def compare_dict_list(expected_list, target_list):
        assert len(expected_list) == len(target_list), \
            "List length is not same: Expect {expected_num} but {target_number}".format(
                expected_num=len(expected_list), target_number=len(target_list))
        CompareUtils().content_list_format(target_list)
        for i in range(len(expected_list)):
            expect_dict = expected_list[i]
            CompareUtils().content_dict_format(expect_dict)
            assert expect_dict in target_list, "Target list miss dict {}".format(str(expect_dict))

    @staticmethod
    def compare_dict_list_without_format(expected_list, target_list):
        assert len(expected_list) == len(target_list), \
            "List length is not same: Expect {expected_num} but {target_number}".format(
                expected_num=len(expected_list), target_number=len(target_list))
        # CompareUtils().content_list_format(target_list)
        for i in range(len(expected_list)):
            expect_dict = expected_list[i]
            # CompareUtils().content_dict_format(expect_dict)
            assert expect_dict in target_list, "Target list miss dict {}".format(str(expect_dict))

    @staticmethod
    def content_dict_format(content_dict):
        for (k, v) in content_dict.items():
            if v is None:
                v = ''
                content_dict[k] = v
                continue
            if "\\n" in v:
                v = v.replace("\\n", "\n")
                content_dict[k] = v

    @staticmethod
    def content_list_format(content_dict_list):
        for content_dict in content_dict_list:
            for (k, v) in content_dict.items():
                if v is None:
                    v = ''
                    content_dict[k] = v
                    continue
                if "\\n" in v:
                    v = v.replace("\\n", "\n")
                    content_dict[k] = v
