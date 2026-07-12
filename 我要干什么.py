import random
import json
import os
if os.name == 'nt':
    os.system('')  # 这会激活 cmd/powershell 的 ANSI 转义支持
class RandomActivitySelector:
    def __init__(self, filename="activities.json"):
        """
        初始化活动选择器
        
        参数:
        filename: 保存活动列表的JSON文件名，默认为"activities.json"
        """
        self.filename = filename
        # 读取已保存的活动列表，如果文件不存在则使用默认活动
        self.activities = self.load_activities()
        # 记录上一次选择的活动，用于避免连续选择相同活动
        self.last_selected = None
    
    def load_activities(self):
        """
        从JSON文件加载活动列表
        
        返回:
        list: 活动列表
        """
        try:
            # 检查文件是否存在
            if os.path.exists(self.filename):
                # 打开并读取JSON文件
                with open(self.filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data.get('activities', [])
            else:
                # 如果文件不存在，返回初始活动列表
                print(f"未找到配置文件 {self.filename}，使用默认活动列表")
                return ['练习vibe coding', '看书', '学英语', '多邻国', '练字', '锻炼']
        except Exception as e:
            # 如果读取文件出错，打印错误信息并返回默认列表
            print(f"读取配置文件时出错: {e}")
            return ['练习vibe coding', '看书', '学英语', '多邻国', '练字', '锻炼']
    
    def save_activities(self):
        """
        将当前活动列表保存到JSON文件
        """
        try:
            # 准备要保存的数据
            data = {
                'activities': self.activities,
                'last_selected': self.last_selected
            }
            # 写入JSON文件
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            # 如果保存文件出错，打印错误信息
            print(f"保存配置文件时出错: {e}")
    
    def add_activity(self, activity):
        """
        添加新活动到列表
        
        参数:
        activity: 要添加的活动名称
        """
        # 检查活动是否已经存在，避免重复添加
        if activity not in self.activities:
            self.activities.append(activity)
            # 保存更新后的活动列表到文件
            self.save_activities()
            print(f"'{activity}' 已添加到活动列表")
        else:
            print(f"'{activity}' 已存在于活动列表中")
    
    def remove_activity(self, activity):
        """
        从列表中移除指定活动
        
        参数:
        activity: 要移除的活动名称
        """
        if activity in self.activities:
            # 检查移除后是否还有其他活动（至少要保留一个）
            if len(self.activities) > 1:
                self.activities.remove(activity)
                # 如果被移除的活动是上一次选择的，则重置last_selected
                if self.last_selected == activity:
                    self.last_selected = None
                # 保存更新后的活动列表到文件
                self.save_activities()
                print(f"'{activity}' 已从活动列表移除")
            else:
                print("无法移除活动：至少需要保留一个活动")
        else:
            print(f"'{activity}' 不存在于活动列表中")
    
    def select_random_activity(self):
        """
        随机选择一个活动，确保与上一次选择不同
        
        返回:
        str: 选中的活动名称
        """
        # 创建可用活动列表，排除上一次选择的活动
        available_activities = [act for act in self.activities if act != self.last_selected]
        
        if not available_activities:
            # 如果没有可用的活动（理论上不应该发生），则从所有活动中选择
            # 这种情况只会在活动列表只有1个元素且该元素就是last_selected时出现
            selected = random.choice(self.activities)
        else:
            # 从可用活动中随机选择一个
            selected = random.choice(available_activities)
        
        # 更新上一次选择的记录
        self.last_selected = selected
        return selected

def main():
    """
    主函数：提供用户交互界面
    """
    # 创建活动选择器实例
    selector = RandomActivitySelector()
    
    print("=" * 50)
    print("欢迎使用随机活动选择器！")
    print("=" * 50)
    
    # 主循环：持续显示菜单直到用户选择退出
    while True:
        print(f"\n当前活动列表 ({len(selector.activities)} 个):")
        # 显示所有活动，每个活动前面加上序号
        for i, activity in enumerate(selector.activities, 1):
            # 标记上一次选择的活动
            marker = " ← 上次选择" if activity == selector.last_selected else ""
            print(f"{i}. {activity}{marker}")
        
        print("\n请选择一个选项:")
        print("1. 🎲 随机选择一个活动")
        print("2. ➕ 添加活动")
        print("3. ➖ 移除活动")
        print("4. 📋 查看活动列表")
        print("5. 🚪 退出程序")
        
        # 获取用户输入并去除首尾空格
        choice = input("\n请输入你的选择 (1-5): ").strip()
        
        if choice == '1':
            # 随机选择活动
            if len(selector.activities) == 0:
                print("活动列表为空，请先添加活动！")
                continue
            
            activity = selector.select_random_activity()
            print(f"🎲 本次选择的活动是: \033[31m{activity}\033[0m")
            
        elif choice == '2':
            # 添加活动
            new_activity = input("请输入要添加的活动名称: ").strip()
            if new_activity:  # 检查输入不为空
                selector.add_activity(new_activity)
            else:
                print("❌ 活动名称不能为空")
                
        elif choice == '3':
            # 移除活动
            if len(selector.activities) <= 1:
                print("❌ 至少需要保留一个活动，无法移除更多活动")
                continue
                
            print("当前活动列表:")
            for i, activity in enumerate(selector.activities, 1):
                print(f"{i}. {activity}")
            
            try:
                # 用户可以选择输入活动名称或序号
                user_input = input("请输入要移除的活动名称或序号: ").strip()
                
                # 检查输入的是不是数字（序号）
                if user_input.isdigit():
                    index = int(user_input) - 1  # 转换为数组索引
                    if 0 <= index < len(selector.activities):
                        activity_to_remove = selector.activities[index]
                        selector.remove_activity(activity_to_remove)
                    else:
                        print("❌ 序号超出范围")
                else:
                    # 输入的是活动名称
                    selector.remove_activity(user_input)
                    
            except ValueError:
                print("❌ 无效输入")
                
        elif choice == '4':
            # 查看活动列表（与主菜单显示相同）
            print(f"\n📋 当前活动列表 ({len(selector.activities)} 个):")
            for i, activity in enumerate(selector.activities, 1):
                marker = " ← 上次选择" if activity == selector.last_selected else ""
                print(f"{i}. {activity}{marker}")
                
        elif choice == '5':
            # 退出程序
            print("👋 感谢使用随机活动选择器，再见！")
            break
            
        else:
            # 处理无效输入
            print("❌ 无效的选择，请输入 1-5 之间的数字")

# 程序入口点：只有直接运行此脚本时才执行main函数
if __name__ == "__main__":
    main()