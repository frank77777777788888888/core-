#!/usr/bin/env python3
"""
OpenHands每日学习计划生成器
基于当前进度和OpenHands复现目标，生成个性化每日学习计划
"""

import json
import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass
import random

@dataclass
class OpenHandsTask:
    """OpenHands学习任务"""
    task_type: str  # code_analysis, implementation, testing, optimization, documentation
    title: str
    description: str
    target_files: List[str]  # 目标文件
    estimated_time: int  # 分钟
    difficulty: str  # easy, medium, hard
    prerequisites: List[str]
    success_criteria: str
    learning_objectives: List[str]

@dataclass
class DailyOpenHandsPlan:
    """每日OpenHands学习计划"""
    date: str
    current_phase: str
    focus_skill: str
    target_files: List[str]
    total_time: int  # 分钟
    tasks: List[OpenHandsTask]
    code_analysis_goal: int  # 目标分析代码行数
    implementation_goal: str  # 实现目标
    motivation_quote: str

class OpenHandsLearningPlanner:
    """OpenHands学习计划生成器"""
    
    def __init__(self):
        self.skill_focus_map = self._load_skill_focus_map()
        self.file_learning_map = self._load_file_learning_map()
        self.motivation_quotes = self._load_motivation_quotes()
        self.task_templates = self._load_task_templates()
    
    def _load_skill_focus_map(self) -> Dict[str, Dict]:
        """加载技能重点映射"""
        return {
            # 架构理解期技能
            "代码结构分析": {
                "priority_files": [
                    "openhands/core/main.py",
                    "openhands/core/loop.py", 
                    "openhands/core/__init__.py",
                    "openhands/agenthub/__init__.py",
                    "openhands/runtime/__init__.py"
                ],
                "analysis_focus": ["模块依赖", "数据流向", "控制流程", "接口设计"],
                "daily_goals": ["分析100行核心代码", "绘制模块关系图", "理解设计模式"]
            },
            "消息事件系统": {
                "priority_files": [
                    "openhands/core/message.py",
                    "openhands/core/message_utils.py",
                    "openhands/events/action/",
                    "openhands/events/observation/",
                    "openhands/core/schema/action.py"
                ],
                "analysis_focus": ["事件驱动架构", "消息序列化", "异步处理", "事件路由"],
                "daily_goals": ["理解事件类型", "分析消息流程", "实现简单事件系统"]
            },
            "Agent抽象设计": {
                "priority_files": [
                    "openhands/core/schema/agent.py",
                    "openhands/agenthub/codeact_agent/",
                    "openhands/agenthub/planner_agent/",
                    "openhands/core/loop.py"
                ],
                "analysis_focus": ["Agent抽象", "策略模式", "生命周期", "状态管理"],
                "daily_goals": ["理解Agent接口", "分析Agent实现", "设计Agent基类"]
            },
            
            # 核心功能复现期技能
            "LLM集成系统": {
                "priority_files": [
                    "openhands/llm/llm.py",
                    "openhands/llm/openai_llm.py",
                    "openhands/llm/anthropic_llm.py",
                    "openhands/core/config/llm_config.py"
                ],
                "analysis_focus": ["LLM抽象", "API调用", "流式响应", "模型路由"],
                "daily_goals": ["理解LLM接口", "分析API集成", "实现模型适配器"]
            },
            "工具调用系统": {
                "priority_files": [
                    "openhands/agenthub/codeact_agent/function_calling.py",
                    "openhands/agenthub/codeact_agent/tools/",
                    "openhands/agenthub/planner_agent/tools/"
                ],
                "analysis_focus": ["工具抽象", "动态调用", "安全机制", "结果处理"],
                "daily_goals": ["理解工具接口", "分析调用机制", "实现工具注册"]
            },
            "运行时环境": {
                "priority_files": [
                    "openhands/runtime/runtime.py",
                    "openhands/runtime/docker/",
                    "openhands/runtime/sandbox/",
                    "openhands/security/"
                ],
                "analysis_focus": ["容器化", "进程管理", "文件系统", "安全隔离"],
                "daily_goals": ["理解运行时架构", "分析Docker集成", "实现沙箱环境"]
            },
            
            # 高级特性掌握期技能
            "微Agent系统": {
                "priority_files": [
                    "microagents/",
                    "openhands/microagent/",
                    "microagents/README.md"
                ],
                "analysis_focus": ["微Agent设计", "模板系统", "工作流", "专用化"],
                "daily_goals": ["理解微Agent概念", "分析模板机制", "实现专用Agent"]
            },
            "MCP协议集成": {
                "priority_files": [
                    "openhands/mcp/",
                    "openhands/mcp/mcp_client.py"
                ],
                "analysis_focus": ["协议规范", "消息格式", "上下文管理", "网络通信"],
                "daily_goals": ["理解MCP协议", "分析消息格式", "实现协议解析"]
            }
        }
    
    def _load_file_learning_map(self) -> Dict[str, Dict]:
        """加载文件学习映射"""
        return {
            "openhands/core/main.py": {
                "learning_objectives": ["理解程序入口", "掌握初始化流程", "学习配置加载"],
                "key_concepts": ["程序启动", "配置管理", "依赖注入"],
                "analysis_points": ["main函数逻辑", "配置解析", "组件初始化"]
            },
            "openhands/core/loop.py": {
                "learning_objectives": ["理解主控制循环", "掌握事件处理", "学习状态管理"],
                "key_concepts": ["控制循环", "事件驱动", "状态机"],
                "analysis_points": ["循环逻辑", "事件分发", "状态转换"]
            },
            "openhands/core/message.py": {
                "learning_objectives": ["理解消息抽象", "掌握序列化", "学习消息路由"],
                "key_concepts": ["消息模式", "序列化", "路由机制"],
                "analysis_points": ["消息基类", "序列化方法", "路由逻辑"]
            },
            "openhands/llm/llm.py": {
                "learning_objectives": ["理解LLM抽象", "掌握API设计", "学习异步调用"],
                "key_concepts": ["抽象类", "API设计", "异步编程"],
                "analysis_points": ["抽象方法", "接口定义", "异步实现"]
            }
        }
    
    def _load_motivation_quotes(self) -> List[str]:
        """加载激励语录"""
        return [
            "🚀 今天分析的每一行OpenHands代码，都是通往AI Agent专家的阶梯！",
            "💡 理解OpenHands的设计思想，就是在学习顶级工程师的智慧！",
            "🎯 复现OpenHands不仅是技术挑战，更是职业生涯的重要里程碑！",
            "⚡ 掌握OpenHands的核心技术，就是掌握AI Agent的未来！",
            "🌟 每个模块的深入理解，都让你离顶级AI工程师更近一步！",
            "🔥 OpenHands的每个设计细节，都蕴含着宝贵的工程经验！",
            "🎨 用代码复现OpenHands，用理解超越OpenHands！",
            "🏆 今天的深度学习，就是明天的技术优势！",
            "💪 挑战OpenHands的复杂度，提升自己的技术深度！",
            "🌈 在OpenHands的代码海洋中，发现AI Agent的技术宝藏！"
        ]
    
    def _load_task_templates(self) -> Dict[str, Dict]:
        """加载任务模板"""
        return {
            "code_analysis": {
                "easy": {
                    "time_range": (30, 45),
                    "description_template": "分析{file}的基础结构和主要功能",
                    "success_criteria": "理解文件的主要作用和基本结构"
                },
                "medium": {
                    "time_range": (45, 60),
                    "description_template": "深入分析{file}的设计模式和实现细节",
                    "success_criteria": "理解设计思路和实现原理"
                },
                "hard": {
                    "time_range": (60, 90),
                    "description_template": "全面分析{file}的架构设计和优化策略",
                    "success_criteria": "掌握架构设计和能够提出改进建议"
                }
            },
            "implementation": {
                "easy": {
                    "time_range": (45, 60),
                    "description_template": "实现{feature}的基础功能",
                    "success_criteria": "基础功能正常工作"
                },
                "medium": {
                    "time_range": (60, 90),
                    "description_template": "完整实现{feature}并添加错误处理",
                    "success_criteria": "功能完整且健壮"
                },
                "hard": {
                    "time_range": (90, 120),
                    "description_template": "实现{feature}并进行性能优化",
                    "success_criteria": "功能完整且性能优秀"
                }
            },
            "testing": {
                "easy": {
                    "time_range": (30, 45),
                    "description_template": "为{component}编写基础单元测试",
                    "success_criteria": "测试覆盖主要功能"
                },
                "medium": {
                    "time_range": (45, 60),
                    "description_template": "为{component}编写完整的测试套件",
                    "success_criteria": "测试覆盖率达到80%以上"
                }
            }
        }
    
    def analyze_current_progress(self, skill_tracker) -> Dict[str, any]:
        """分析当前学习进度"""
        # 找出当前阶段
        phase_progress = skill_tracker.get_phase_progress()
        current_phase = None
        for phase, data in phase_progress.items():
            completion_rate = float(data["完成率"].rstrip('%'))
            if completion_rate < 80:
                current_phase = phase
                break
        
        if not current_phase:
            current_phase = "创新突破期"  # 如果都完成了，进入创新期
        
        # 找出该阶段最需要提升的技能
        phase_skills = [skill for skill in skill_tracker.skills.values() 
                       if skill.phase == current_phase and skill.current_score < skill.target_score]
        
        focus_skill = None
        if phase_skills:
            # 按权重和差距排序
            phase_skills.sort(key=lambda x: (x.target_score - x.current_score) * x.weight / 100, reverse=True)
            focus_skill = phase_skills[0].skill_name
        
        return {
            "current_phase": current_phase,
            "focus_skill": focus_skill,
            "phase_skills": phase_skills
        }
    
    def generate_code_analysis_task(self, skill_name: str, difficulty: str, target_files: List[str]) -> OpenHandsTask:
        """生成代码分析任务"""
        template = self.task_templates["code_analysis"][difficulty]
        time_range = template["time_range"]
        
        # 选择目标文件
        if target_files:
            target_file = target_files[0]
        else:
            target_file = "核心文件"
        
        file_info = self.file_learning_map.get(target_file, {})
        learning_objectives = file_info.get("learning_objectives", ["理解代码结构", "掌握实现原理"])
        
        return OpenHandsTask(
            task_type="code_analysis",
            title=f"{skill_name} - 代码分析",
            description=template["description_template"].format(file=target_file),
            target_files=[target_file] if target_file != "核心文件" else [],
            estimated_time=random.randint(*time_range),
            difficulty=difficulty,
            prerequisites=["代码阅读能力", "相关技术基础"],
            success_criteria=template["success_criteria"],
            learning_objectives=learning_objectives
        )
    
    def generate_implementation_task(self, skill_name: str, difficulty: str) -> OpenHandsTask:
        """生成实现任务"""
        template = self.task_templates["implementation"][difficulty]
        time_range = template["time_range"]
        
        # 根据技能确定实现目标
        feature_map = {
            "消息事件系统": "事件处理器",
            "Agent抽象设计": "Agent基类",
            "LLM集成系统": "LLM适配器",
            "工具调用系统": "工具注册器",
            "运行时环境": "代码执行器",
            "微Agent系统": "微Agent框架",
            "MCP协议集成": "协议解析器"
        }
        
        feature = feature_map.get(skill_name, "相关功能")
        
        return OpenHandsTask(
            task_type="implementation",
            title=f"{skill_name} - 功能实现",
            description=template["description_template"].format(feature=feature),
            target_files=[],
            estimated_time=random.randint(*time_range),
            difficulty=difficulty,
            prerequisites=["编程基础", "相关技术理解"],
            success_criteria=template["success_criteria"],
            learning_objectives=[f"实现{feature}", "掌握实现技巧", "提升编程能力"]
        )
    
    def generate_testing_task(self, skill_name: str, difficulty: str) -> OpenHandsTask:
        """生成测试任务"""
        template = self.task_templates["testing"][difficulty]
        time_range = template["time_range"]
        
        component = skill_name.replace("系统", "").replace("设计", "")
        
        return OpenHandsTask(
            task_type="testing",
            title=f"{skill_name} - 测试编写",
            description=template["description_template"].format(component=component),
            target_files=[],
            estimated_time=random.randint(*time_range),
            difficulty=difficulty,
            prerequisites=["测试框架", "单元测试"],
            success_criteria=template["success_criteria"],
            learning_objectives=["编写测试用例", "提高代码质量", "掌握测试技巧"]
        )
    
    def generate_optimization_task(self, skill_name: str) -> OpenHandsTask:
        """生成优化任务"""
        return OpenHandsTask(
            task_type="optimization",
            title=f"{skill_name} - 性能优化",
            description=f"分析并优化{skill_name}的性能瓶颈",
            target_files=[],
            estimated_time=random.randint(60, 90),
            difficulty="hard",
            prerequisites=["性能分析", "优化技巧"],
            success_criteria="性能提升明显，优化效果可量化",
            learning_objectives=["识别性能瓶颈", "掌握优化技巧", "提升系统性能"]
        )
    
    def generate_daily_plan(self, skill_tracker, available_time: int = 240) -> DailyOpenHandsPlan:
        """生成每日学习计划"""
        # 分析当前进度
        progress_info = self.analyze_current_progress(skill_tracker)
        current_phase = progress_info["current_phase"]
        focus_skill = progress_info["focus_skill"]
        
        if not focus_skill:
            focus_skill = "代码结构分析"  # 默认技能
        
        # 获取技能相关信息
        skill_info = self.skill_focus_map.get(focus_skill, {})
        target_files = skill_info.get("priority_files", [])
        daily_goals = skill_info.get("daily_goals", ["深入学习相关技术"])
        
        # 生成任务列表
        tasks = []
        remaining_time = available_time
        
        # 根据可用时间分配任务
        if remaining_time >= 180:  # 3小时以上
            # 代码分析 + 实现 + 测试
            tasks.append(self.generate_code_analysis_task(focus_skill, "medium", target_files))
            tasks.append(self.generate_implementation_task(focus_skill, "medium"))
            tasks.append(self.generate_testing_task(focus_skill, "easy"))
        elif remaining_time >= 120:  # 2小时
            # 代码分析 + 实现
            tasks.append(self.generate_code_analysis_task(focus_skill, "medium", target_files))
            tasks.append(self.generate_implementation_task(focus_skill, "easy"))
        elif remaining_time >= 90:  # 1.5小时
            # 深度代码分析 + 简单实现
            tasks.append(self.generate_code_analysis_task(focus_skill, "hard", target_files))
            tasks.append(self.generate_implementation_task(focus_skill, "easy"))
        else:  # 1.5小时以下
            # 专注代码分析
            tasks.append(self.generate_code_analysis_task(focus_skill, "medium", target_files))
        
        # 调整任务时间以适应可用时间
        total_task_time = sum(task.estimated_time for task in tasks)
        if total_task_time > available_time:
            scale_factor = available_time / total_task_time
            for task in tasks:
                task.estimated_time = int(task.estimated_time * scale_factor)
        
        # 设置代码分析目标
        code_analysis_goal = 100 if available_time >= 120 else 50
        
        # 设置实现目标
        implementation_goal = daily_goals[0] if daily_goals else "理解核心概念"
        
        return DailyOpenHandsPlan(
            date=datetime.datetime.now().strftime("%Y-%m-%d"),
            current_phase=current_phase,
            focus_skill=focus_skill,
            target_files=target_files[:3],  # 限制文件数量
            total_time=sum(task.estimated_time for task in tasks),
            tasks=tasks,
            code_analysis_goal=code_analysis_goal,
            implementation_goal=implementation_goal,
            motivation_quote=random.choice(self.motivation_quotes)
        )
    
    def format_daily_plan(self, plan: DailyOpenHandsPlan) -> str:
        """格式化每日计划输出"""
        output = []
        output.append(f"📅 {plan.date} OpenHands学习计划")
        output.append("=" * 60)
        output.append(f"\n🎯 当前阶段: {plan.current_phase}")
        output.append(f"🔥 重点技能: {plan.focus_skill}")
        output.append(f"⏰ 总学习时间: {plan.total_time}分钟")
        output.append(f"📊 代码分析目标: {plan.code_analysis_goal}行")
        output.append(f"🎯 实现目标: {plan.implementation_goal}")
        output.append(f"\n{plan.motivation_quote}")
        
        if plan.target_files:
            output.append(f"\n📁 重点文件:")
            for file in plan.target_files:
                output.append(f"  • {file}")
        
        output.append("\n📋 学习任务清单:")
        for i, task in enumerate(plan.tasks, 1):
            output.append(f"\n{i}. {task.title}")
            output.append(f"   📝 内容: {task.description}")
            output.append(f"   ⏱️  时间: {task.estimated_time}分钟")
            output.append(f"   📊 难度: {task.difficulty}")
            if task.target_files:
                output.append(f"   📁 目标文件: {', '.join(task.target_files)}")
            output.append(f"   🎯 学习目标: {', '.join(task.learning_objectives[:2])}")
            output.append(f"   ✅ 成功标准: {task.success_criteria}")
        
        output.append("\n💡 学习建议:")
        output.append("• 先通读目标文件，理解整体结构")
        output.append("• 重点分析核心类和关键方法")
        output.append("• 边分析边做笔记，记录设计思路")
        output.append("• 实现时参考原版代码的设计模式")
        output.append("• 完成后对比分析差异和改进点")
        
        output.append("\n🎯 今日目标:")
        output.append(f"• 深入理解 {plan.focus_skill} 的实现原理")
        output.append(f"• 分析至少 {plan.code_analysis_goal} 行OpenHands代码")
        output.append(f"• 完成 {plan.implementation_goal}")
        output.append("• 记录学习心得和技术洞察")
        
        return "\n".join(output)
    
    def generate_weekly_focus(self, skill_tracker) -> str:
        """生成周重点概览"""
        progress_info = self.analyze_current_progress(skill_tracker)
        current_phase = progress_info["current_phase"]
        phase_skills = progress_info["phase_skills"]
        
        output = []
        output.append(f"📊 本周OpenHands学习重点 - {current_phase}")
        output.append("=" * 50)
        
        if phase_skills:
            output.append(f"\n🎯 本阶段待完成技能 ({len(phase_skills)}个):")
            for i, skill in enumerate(phase_skills[:5], 1):  # 显示前5个
                gap = skill.target_score - skill.current_score
                weight_info = f"权重{skill.weight}%"
                output.append(f"{i}. {skill.skill_name} - 差距{gap}分 ({weight_info})")
                
                # 显示关键文件
                skill_info = self.skill_focus_map.get(skill.skill_name, {})
                priority_files = skill_info.get("priority_files", [])
                if priority_files:
                    output.append(f"   📁 重点文件: {', '.join(priority_files[:2])}")
        
        output.append(f"\n📅 本周建议安排:")
        output.append("• 周一-周二: 深度代码分析，理解设计思路")
        output.append("• 周三-周四: 功能实现，参考原版设计")
        output.append("• 周五: 测试验证，性能对比分析")
        output.append("• 周末: 总结复习，准备下周内容")
        
        output.append(f"\n🎯 本周目标:")
        output.append("• 完成当前重点技能的深度学习")
        output.append("• 分析500+行OpenHands核心代码")
        output.append("• 实现1-2个核心功能模块")
        output.append("• 编写技术总结和学习心得")
        
        return "\n".join(output)

def main():
    """主函数 - 演示使用"""
    from openhands_skill_tracker import OpenHandsSkillTracker
    
    # 初始化
    skill_tracker = OpenHandsSkillTracker()
    planner = OpenHandsLearningPlanner()
    
    print("🎯 OpenHands每日学习计划生成器")
    print("=" * 60)
    
    # 生成今日计划
    daily_plan = planner.generate_daily_plan(skill_tracker, available_time=240)
    print(planner.format_daily_plan(daily_plan))
    
    print("\n" + "=" * 60)
    
    # 生成周概览
    weekly_focus = planner.generate_weekly_focus(skill_tracker)
    print(weekly_focus)
    
    print("\n" + "=" * 60)
    print("💡 使用建议:")
    print("1. 每天运行生成OpenHands学习计划")
    print("2. 重点分析指定的目标文件")
    print("3. 实现功能时参考原版设计思路")
    print("4. 完成任务后及时更新技能分数")
    print("5. 定期总结学习心得和技术洞察")

if __name__ == "__main__":
    main()