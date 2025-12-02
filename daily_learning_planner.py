#!/usr/bin/env python3
"""
AI Agent学习每日计划生成器
基于当前技能水平和目标，自动生成个性化学习计划
"""

import json
import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass
import random

@dataclass
class LearningTask:
    """学习任务"""
    task_type: str  # theory, practice, project, review
    title: str
    description: str
    estimated_time: int  # 分钟
    difficulty: str  # easy, medium, hard
    resources: List[str]
    success_criteria: str

@dataclass
class DailyPlan:
    """每日学习计划"""
    date: str
    focus_skill: str
    total_time: int  # 分钟
    tasks: List[LearningTask]
    motivation_quote: str

class LearningPlanner:
    """学习计划生成器"""
    
    def __init__(self):
        self.skill_priorities = self._load_skill_priorities()
        self.learning_resources = self._load_learning_resources()
        self.motivation_quotes = self._load_motivation_quotes()
    
    def _load_skill_priorities(self) -> Dict[str, int]:
        """加载技能优先级配置"""
        return {
            # 基础建设期技能 (优先级1-5)
            "Python高级特性": 5,
            "PyTorch深度学习": 5,
            "大模型API集成": 4,
            "LangChain框架": 4,
            "向量数据库": 3,
            
            # 核心技能期技能 (优先级6-10)
            "多Agent系统架构": 10,
            "强化学习算法": 9,
            "RLHF实现": 8,
            "分布式系统设计": 7,
            "模型部署优化": 6,
            "AI安全防护": 6,
            
            # 专家精进期技能 (优先级11-15)
            "神经符号融合": 8,
            "具身智能": 7,
            "大规模系统架构": 9,
            "技术团队管理": 6,
            "创新研究能力": 8,
        }
    
    def _load_learning_resources(self) -> Dict[str, Dict]:
        """加载学习资源库"""
        return {
            "Python高级特性": {
                "theory": [
                    "《流畅的Python》第7-9章",
                    "Python官方文档 - 高级特性",
                    "Real Python - Advanced Python Features"
                ],
                "practice": [
                    "实现装饰器模式",
                    "编写异步爬虫",
                    "设计元类应用"
                ],
                "projects": [
                    "构建异步Web框架",
                    "开发代码生成工具",
                    "实现ORM框架"
                ]
            },
            "PyTorch深度学习": {
                "theory": [
                    "《深度学习》- Ian Goodfellow",
                    "PyTorch官方教程",
                    "CS231n课程视频"
                ],
                "practice": [
                    "手写反向传播算法",
                    "实现常见网络层",
                    "自定义损失函数"
                ],
                "projects": [
                    "图像分类模型",
                    "文本生成模型",
                    "强化学习环境"
                ]
            },
            "多Agent系统架构": {
                "theory": [
                    "《多智能体系统》教材",
                    "AAMAS会议论文",
                    "分布式系统设计模式"
                ],
                "practice": [
                    "实现Agent通信协议",
                    "设计任务分配算法",
                    "构建协调机制"
                ],
                "projects": [
                    "多Agent游戏AI",
                    "分布式优化系统",
                    "智能交通控制"
                ]
            },
            "强化学习算法": {
                "theory": [
                    "《强化学习：原理与Python实现》",
                    "Sutton & Barto教材",
                    "OpenAI Spinning Up"
                ],
                "practice": [
                    "实现Q-Learning",
                    "编写Policy Gradient",
                    "调试PPO算法"
                ],
                "projects": [
                    "游戏AI训练",
                    "机器人控制",
                    "推荐系统优化"
                ]
            }
        }
    
    def _load_motivation_quotes(self) -> List[str]:
        """加载激励语录"""
        return [
            "🚀 每一行代码都是通往AI未来的阶梯！",
            "💡 今天的学习，就是明天的竞争优势！",
            "🎯 专注当下，成就未来的AI专家！",
            "⚡ 技术的边界，就是想象力的边界！",
            "🌟 在AI的黄金时代，做最闪亮的那颗星！",
            "🔥 每个算法的掌握，都是实力的积累！",
            "🎨 用代码创造智能，用智能改变世界！",
            "🏆 今天比昨天更强，明天比今天更优秀！",
            "💪 困难只是成长路上的垫脚石！",
            "🌈 学习的路虽然艰辛，但终点是彩虹！"
        ]
    
    def analyze_current_skills(self, skill_tracker) -> Dict[str, int]:
        """分析当前技能水平"""
        skill_gaps = {}
        for skill_name, skill_data in skill_tracker.skills.items():
            gap = skill_data.target_score - skill_data.current_score
            if gap > 0:
                skill_gaps[skill_name] = gap
        return skill_gaps
    
    def select_focus_skill(self, skill_gaps: Dict[str, int]) -> str:
        """选择今日重点技能"""
        if not skill_gaps:
            return "技能复习"
        
        # 综合考虑技能差距和优先级
        weighted_scores = {}
        for skill, gap in skill_gaps.items():
            priority = self.skill_priorities.get(skill, 1)
            weighted_scores[skill] = gap * priority
        
        # 选择权重最高的技能
        focus_skill = max(weighted_scores, key=weighted_scores.get)
        return focus_skill
    
    def generate_theory_task(self, skill: str, difficulty: str) -> LearningTask:
        """生成理论学习任务"""
        resources = self.learning_resources.get(skill, {}).get("theory", ["相关理论资料"])
        
        if difficulty == "easy":
            time_range = (30, 45)
            task_desc = f"阅读{skill}基础概念和原理"
        elif difficulty == "medium":
            time_range = (45, 60)
            task_desc = f"深入学习{skill}核心算法和实现"
        else:  # hard
            time_range = (60, 90)
            task_desc = f"研究{skill}前沿论文和最新进展"
        
        return LearningTask(
            task_type="theory",
            title=f"{skill} - 理论学习",
            description=task_desc,
            estimated_time=random.randint(*time_range),
            difficulty=difficulty,
            resources=resources[:2],  # 限制资源数量
            success_criteria="理解核心概念，能够向他人解释"
        )
    
    def generate_practice_task(self, skill: str, difficulty: str) -> LearningTask:
        """生成实践练习任务"""
        practices = self.learning_resources.get(skill, {}).get("practice", ["相关练习"])
        
        if difficulty == "easy":
            time_range = (45, 60)
            practice = practices[0] if practices else "基础练习"
        elif difficulty == "medium":
            time_range = (60, 90)
            practice = practices[1] if len(practices) > 1 else "中级练习"
        else:  # hard
            time_range = (90, 120)
            practice = practices[2] if len(practices) > 2 else "高级练习"
        
        return LearningTask(
            task_type="practice",
            title=f"{skill} - 编程实践",
            description=f"完成练习：{practice}",
            estimated_time=random.randint(*time_range),
            difficulty=difficulty,
            resources=["IDE环境", "相关文档", "示例代码"],
            success_criteria="代码运行正确，通过测试用例"
        )
    
    def generate_project_task(self, skill: str, difficulty: str) -> LearningTask:
        """生成项目任务"""
        projects = self.learning_resources.get(skill, {}).get("projects", ["相关项目"])
        
        if difficulty == "easy":
            time_range = (60, 90)
            project = f"简化版{projects[0]}" if projects else "入门项目"
        elif difficulty == "medium":
            time_range = (90, 120)
            project = projects[0] if projects else "中级项目"
        else:  # hard
            time_range = (120, 180)
            project = f"完整{projects[0]}" if projects else "高级项目"
        
        return LearningTask(
            task_type="project",
            title=f"{skill} - 项目开发",
            description=f"开发项目：{project}",
            estimated_time=random.randint(*time_range),
            difficulty=difficulty,
            resources=["开发环境", "项目模板", "技术文档"],
            success_criteria="项目功能完整，代码质量良好"
        )
    
    def generate_review_task(self, skill: str) -> LearningTask:
        """生成复习任务"""
        return LearningTask(
            task_type="review",
            title=f"{skill} - 知识复习",
            description=f"复习{skill}的核心概念和实现要点",
            estimated_time=30,
            difficulty="easy",
            resources=["学习笔记", "代码示例", "思维导图"],
            success_criteria="能够快速回忆关键知识点"
        )
    
    def generate_daily_plan(self, skill_tracker, available_time: int = 180) -> DailyPlan:
        """生成每日学习计划"""
        # 分析技能差距
        skill_gaps = self.analyze_current_skills(skill_tracker)
        
        # 选择重点技能
        focus_skill = self.select_focus_skill(skill_gaps)
        
        # 生成任务列表
        tasks = []
        remaining_time = available_time
        
        # 根据可用时间分配任务
        if remaining_time >= 120:  # 2小时以上
            # 理论 + 实践 + 项目
            tasks.append(self.generate_theory_task(focus_skill, "medium"))
            tasks.append(self.generate_practice_task(focus_skill, "medium"))
            tasks.append(self.generate_project_task(focus_skill, "easy"))
        elif remaining_time >= 90:  # 1.5小时
            # 理论 + 实践
            tasks.append(self.generate_theory_task(focus_skill, "medium"))
            tasks.append(self.generate_practice_task(focus_skill, "medium"))
        elif remaining_time >= 60:  # 1小时
            # 实践为主
            tasks.append(self.generate_practice_task(focus_skill, "medium"))
            tasks.append(self.generate_review_task(focus_skill))
        else:  # 1小时以下
            # 理论学习
            tasks.append(self.generate_theory_task(focus_skill, "easy"))
        
        # 调整任务时间以适应可用时间
        total_task_time = sum(task.estimated_time for task in tasks)
        if total_task_time > available_time:
            # 按比例缩减时间
            scale_factor = available_time / total_task_time
            for task in tasks:
                task.estimated_time = int(task.estimated_time * scale_factor)
        
        return DailyPlan(
            date=datetime.datetime.now().strftime("%Y-%m-%d"),
            focus_skill=focus_skill,
            total_time=sum(task.estimated_time for task in tasks),
            tasks=tasks,
            motivation_quote=random.choice(self.motivation_quotes)
        )
    
    def format_daily_plan(self, plan: DailyPlan) -> str:
        """格式化每日计划输出"""
        output = []
        output.append(f"📅 {plan.date} AI Agent学习计划")
        output.append("=" * 50)
        output.append(f"\n🎯 今日重点技能: {plan.focus_skill}")
        output.append(f"⏰ 总学习时间: {plan.total_time}分钟")
        output.append(f"\n{plan.motivation_quote}")
        
        output.append("\n📋 学习任务清单:")
        for i, task in enumerate(plan.tasks, 1):
            output.append(f"\n{i}. {task.title}")
            output.append(f"   📝 内容: {task.description}")
            output.append(f"   ⏱️  时间: {task.estimated_time}分钟")
            output.append(f"   📊 难度: {task.difficulty}")
            output.append(f"   📚 资源: {', '.join(task.resources[:2])}")
            output.append(f"   ✅ 成功标准: {task.success_criteria}")
        
        output.append("\n💡 学习建议:")
        output.append("• 保持专注，避免多任务干扰")
        output.append("• 理论学习后立即进行实践")
        output.append("• 记录学习笔记和遇到的问题")
        output.append("• 完成后更新技能评估分数")
        
        output.append("\n🎯 今日目标:")
        output.append(f"• 提升 {plan.focus_skill} 技能水平")
        output.append("• 完成所有计划任务")
        output.append("• 记录学习成果和心得")
        
        return "\n".join(output)
    
    def generate_weekly_overview(self, skill_tracker) -> str:
        """生成周学习概览"""
        skill_gaps = self.analyze_current_skills(skill_tracker)
        
        # 选择本周重点技能（前5个）
        sorted_skills = sorted(skill_gaps.items(), 
                             key=lambda x: x[1] * self.skill_priorities.get(x[0], 1), 
                             reverse=True)[:5]
        
        output = []
        output.append("📊 本周学习重点概览")
        output.append("=" * 40)
        
        for i, (skill, gap) in enumerate(sorted_skills, 1):
            priority = self.skill_priorities.get(skill, 1)
            output.append(f"\n{i}. {skill}")
            output.append(f"   差距: {gap}分 | 优先级: {priority}")
            
            # 建议学习时间分配
            if i <= 2:
                time_allocation = "每天60-90分钟"
            elif i <= 4:
                time_allocation = "每天30-45分钟"
            else:
                time_allocation = "每天15-30分钟"
            
            output.append(f"   建议时间: {time_allocation}")
        
        output.append("\n🎯 本周目标:")
        output.append("• 重点突破前2个技能")
        output.append("• 保持其他技能的练习")
        output.append("• 完成至少1个实践项目")
        output.append("• 更新技能评估和进度")
        
        return "\n".join(output)

def main():
    """主函数 - 演示使用"""
    from skill_assessment_tracker import SkillTracker
    
    # 初始化
    skill_tracker = SkillTracker()
    planner = LearningPlanner()
    
    print("🎯 AI Agent每日学习计划生成器")
    print("=" * 50)
    
    # 生成今日计划
    daily_plan = planner.generate_daily_plan(skill_tracker, available_time=180)
    print(planner.format_daily_plan(daily_plan))
    
    print("\n" + "=" * 50)
    
    # 生成周概览
    weekly_overview = planner.generate_weekly_overview(skill_tracker)
    print(weekly_overview)
    
    print("\n" + "=" * 50)
    print("💡 使用建议:")
    print("1. 每天运行生成个性化学习计划")
    print("2. 根据可用时间调整学习任务")
    print("3. 完成任务后及时更新技能分数")
    print("4. 定期查看周概览调整重点")

if __name__ == "__main__":
    main()