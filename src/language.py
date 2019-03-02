# -*- coding: UTF-8 -*-

class language:
    def __init__(self):
        self.language = 0
        print "init"
    def get_title_name(self):
        if self.language == 1:
            return "a80"
        else:
            return "工具"
    def get_filemerge_box_title(self):
        if self.language == 1:
            return "FileMerge"
        else:
            return "文件合并"
    def get_filemerge_file_msg(self):
        if self.language == 1:
            return "File is empty"
        else:
            return "选择所要合并的文件"
    def get_filemerge_svfile_msg(self):
        if self.language == 1:
            return "Save Path is empty"
        else:
            return "选择合并后的文件路径"
    def get_filemerge_box_merge_msg(self):
        if self.language == 1:
            return "Merge Success"
        else:
            return "合并成功"
    def get_filemerge_box_offset_msg(self):
        if self.language == 1:
            return "Offset is Wrong"
        else:
            return "偏移地址错误"
    def get_download_box_title(self):
        if self.language == 1:
            return "Download"
        else:
            return "下载"
    def get_download_box_message(self):
        if self.language == 1:
            return 'You shoud choose download file!!'
        else:
            return "选择所要下载的文件"
    def get_utils_box_title(self):
        if self.language == 1:
            return "Utils"
        else:
            return "写号"
    def get_utils_box_sn_exam(self):
        if self.language == 1:
            return "SN:DW000001"
        else:
            return "序列号8位:DW000001"
    def get_utils_box_sn_length(self):
        if self.language == 1:
            return "SN need 8 bit"
        else:
            return "序列号长度为8位"
    def get_utils_box_act_exam(self):
        if self.language == 1:
            return "ACTCODE:Z3T4Y0GY"
        else:
            return "激活码8位:Z3T4Y0GY"
    def get_utils_box_act_length(self):
        if self.language == 1:
            return "ACT need 8 bit"
        else:
            return "激活码长度为8位"
    def get_utils_box_delayT_min_msg(self):
        if self.language == 1:
            return "Delay Interval >= 60s"
        else:
            return "延时设置最小为60秒"

    def get_utils_box_delayT_msg(self):
        if self.language == 1:
            return "Pls Input DelayTime Unit is S, >=60s"
        else:
            return "延时启动时间单位为秒，最小为60秒"
    def get_utils_box_save_min_msg(self):
        if self.language == 1:
            return "Save Interval >= 60s"
        else:
            return "保存周期最小为60秒"
    def get_utils_box_save_msg(self):
        if self.language == 1:
            return "Pls Input Save Interval Unit is S, >=60s"
        else:
            return "保存周期单位为秒，最小为60秒"
    def get_utils_box_send_min_msg(self):
        if self.language == 1:
            return "Send Interval >= 180s"
        else:
            return "发送周期最小为180秒"
    def get_utils_box_send_msg(self):
        if self.language == 1:
            return "Pls Input Send Interval Unit is S, >=180s"
        else:
            return "发送周期单位为秒，最小为180秒"
    def get_utils_box_no_choose_msg(self):
        if self.language == 1:
            return 'You need to choose one which you want to write!!!'
        else:
            return "必须选择一项进行操作"
    def get_utils_box_imei_length_msg(self):
        if self.language == 1:
            return "The length of IMEI nubmer != 15"
        else:
            return "IMEI号少于15位"
    def get_utils_box_imei_exam_msg(self):
        if self.language == 1:
            return "Input IMEI nubmer as 111111111111119"
        else:
            return "输入IMEI号，如111111111111119"
    def get_feedback_box_title(self):
        if self.language == 1:
            return "FeedBack"
        else:
            return "问题反馈"
    def get_feedback_box_success_msg(self):
        if self.language == 1:
            return "Success"
        else:
            return "提交成功"
    def get_feedback_box_fail_msg(self):
        if self.language == 1:
            return "Faied,Pls try later"
        else:
            return "提交失败，请稍后再试"
    def get_feedback_frame_title(self):
        if self.language == 1:
            return "FeedBack"
        else:
            return "问题反馈"
    def get_filemerge_frame_title(self):
        if self.language == 1:
            return "FileMerge"
        else:
            return "文件合并"
    def get_about_box_title(self):
        if self.language == 1:
            return "About"
        else:
            return "关于"
    def get_tabcontrol_tool_title(self):
        if self.language == 1:
            return "Tool"
        else:
            return "下载"
    def get_tabcontrol_util_title(self):
        if self.language == 1:
            return "Utils"
        else:
            return "写号"
    def get_lbfrm_upgrade_title(self):
        if self.language == 1:
            return "upgrade"
        else:
            return "固件升级"
    def get_bn_choose_title(self):
        if self.language == 1:
            return "Choose"
        else:
            return "选择"
    def get_bn_dl_title(self):
        if self.language == 1:
            return "Download"
        else:
            return "下载"
    def get_bn_merge_title(self):
        if self.language == 1:
            return "Merge"
        else:
            return "合并"
    def get_lb_comm_title(self):
        if self.language == 1:
            return "COMM:"
        else:
            return "下载端口:"
    def get_lb_type_title(self):
        if self.language == 1:
            return "TYPE:"
        else:
            return "类型:"
    def get_lb_appfile_title(self):
        if self.language == 1:
            return "APP File:"
        else:
            return "版本路径:"
    def get_lb_bootfile_title(self):
        if self.language == 1:
            return "BLD File:"
        else:
            return "BLD 路径:"
    def get_bn_get_title(self):
        if self.language == 1:
            return "Get:"
        else:
            return "读取"
    def get_bn_set_title(self):
        if self.language == 1:
            return "Set:"
        else:
            return "写入"
    def get_lb_sn_title(self):
        if self.language == 1:
            return "SN:"
        else:
            return "序列号:"
    def get_lb_act_title(self):
        if self.language == 1:
            return "ACT:"
        else:
            return "激活码:"
    def get_lb_dlt_title(self):
        if self.language == 1:
            return "DelayT:"
        else:
            return "延时启动:"
    def get_lb_svt_title(self):
        if self.language == 1:
            return "SaveT:"
        else:
            return "保存周期:"
    def get_lb_sdt_title(self):
        if self.language == 1:
            return "SendT:"
        else:
            return "发送周期:"
    def get_lb_srst_title(self):
        if self.language == 1:
            return "SystemReset"
        else:
            return "系统重置"
    def get_lb_rdimei_title(self):
        if self.language == 1:
            return "RDIMEI:"
        else:
            return "IMEI读取："
    def get_lb_wrimei_title(self):
        if self.language == 1:
            return "WRIMEI:"
        else:
            return "IMEI写入："
    def get_bn_wrimei_title(self):
        if self.language == 1:
            return "Write"
        else:
            return "写入"
    def get_bn_rdimei_title(self):
        if self.language == 1:
            return "Read"
        else:
            return "读取"
    def get_lb_file1_title(self):
        if self.language == 1:
            return "File1"
        else:
            return "文件1"
    def get_lb_file2_title(self):
        if self.language == 1:
            return "File2"
        else:
            return "文件2"
    def get_lb_offset_title(self):
        if self.language == 1:
            return "Offset"
        else:
            return "偏移"
    def get_lb_tip_title(self):
        if self.language == 1:
            return "Only USB Support!!!"
        else:
            return "仅支持USB操作!!!"
    def get_mn_quit_title(self):
        if self.language == 1:
            return "Quit"
        else:
            return "退出"
    def get_mn_dl_in_standy_title(self):
        if self.language == 1:
            return "Download in StandBy Mode With USB"
        else:
            return "开机状态下进行下载"
    def get_mn_save_log_title(self):
        if self.language == 1:
            return "Save Tool Log"
        else:
            return "保存日志"
    def get_mn_file_merge_title(self):
        if self.language == 1:
            return "FileMerge"
        else:
            return "文件合并"
    def get_mnlb_help_title(self):
        if self.language == 1:
            return "Help"
        else:
            return "帮助"
    def get_mnlb_fdbk_title(self):
        if self.language == 1:
            return "Feedback"
        else:
            return "问题反馈"
    def get_mnlb_abt_title(self):
        if self.language == 1:
            return "About"
        else:
            return "关于"
    def get_mnlb_file_title(self):
        if self.language == 1:
            return "File"
        else:
            return "文件"
    def get_mnlb_option_title(self):
        if self.language == 1:
            return "Option"
        else:
            return "选项"
    def get_bn_send_title(self):
        if self.language == 1:
            return "send"
        else:
            return "发送"