#!/usr/bin/env python3
"""
AI Agent技能掌握度追踪系统
用于量化评估和跟踪学习进度
"""

import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = "入门级"
    INTERMEDIATE = "理解级" 
    PROFICIENT = "熟练级"
    EXPERT = "专家级"

class LearningPhase(Enum):
    FOUNDATION = "基础建设期"
    CORE_SKILLS = "核心技能期"
    EXPERT_LEVEL = "专家精进期"

@dataclass
class SkillAssessment:
    """技能评估记录"""
    skill_name: str
    category: str
    current_score: int  # 0-100
    target_score: int
    last_updated: str
    assessment_notes: str
    learning_resources: List[str]
    practice_projects: List[str]

@dataclass
class ProjectMilestone:
    """项目里程碑"""
    project_name: str
    phase: str
    completion_percentage: int
    key_achievements: List[str]
    technical_challenges: List[str]
    next_steps: List[str]
    deadline: str

class SkillTracker:
    """技能追踪器主类"""
    
    def __init__(self, data_file: str = "skill_progress.json"):
        self.data_file = data_file
        self.skills: Dict[str, SkillAssessment] = {}
        self.projects: Dict[str, ProjectMilestone] = {}
        self.load_data()
    
    def load_data(self):
        """加载历史数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 加载技能数据
                for skill_data in data.get('skills', []):
                    skill = SkillAssessment(**skill_data)
                    self.skills[skill.skill_name] = skill
                # 加载项目数据
                for project_data in data.get('projects', []):
                    project = ProjectMilestone(**project_data)
                    self.projects[project.project_name] = project
        except FileNotFoundError:
            self.initialize_default_skills()
    
    def save_data(self):
        """保存数据到文件"""
        data = {
            'skills': [asdict(skill) for skill in self.skills.values()],
            'projects': [asdict(project) for project in self.projects.values()],
            'last_updated': datetime.datetime.now().isoformat()
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def initialize_default_skills(self):
        """初始化默认技能清单"""
        foundation_skills = [
            ("Python高级特性", "编程基础", 0, 85),
            ("PyTorch深度学习", "机器学习框架", 0, 85),
            ("大模型API集成", "大模型API集成", 0, 80),
            ("LangChain框架", "Agent框架基础", 0, 80),
            ("向量数据库", "Agent框架基础", 0, 75),
        ]
        
        core_skills = [
            ("多Agent系统架构", "多Agent系统架构", 0, 90),
            ("强化学习算法", "强化学习与决策优化", 0, 85),
            ("RLHF实现", "强化学习与决策优化", 0, 85),
            ("分布式系统设计", "高级工程技能", 0, 80),
            ("模型部署优化", "高级工程技能", 0, 80),
            ("AI安全防护", "安全与可靠性", 0, 75),
        ]
        
        expert_skills = [
            ("神经符号融合", "前沿技术研究", 0, 85),
            ("具身智能", "前沿技术研究", 0, 80),
            ("大规模系统架构", "系统架构设计", 0, 90),
            ("技术团队管理", "团队协作与领导", 0, 80),
            ("创新研究能力", "创新与研究", 0, 85),
        ]
        
        all_skills = foundation_skills + core_skills + expert_skills
        
        for skill_name, category, current, target in all_skills:
            self.skills[skill_name] = SkillAssessment(
                skill_name=skill_name,
                category=category,
                current_score=current,
                target_score=target,
                last_updated=datetime.datetime.now().isoformat(),
                assessment_notes="待开始学习",
                learning_resources=[],
                practice_projects=[]
            )
    
    def update_skill_score(self, skill_name: str, new_score: int, notes: str = ""):
        """更新技能分数"""
        if skill_name in self.skills:
            self.skills[skill_name].current_score = new_score
            self.skills[skill_name].last_updated = datetime.datetime.now().isoformat()
            if notes:
                self.skills[skill_name].assessment_notes = notes
            self.save_data()
            print(f"✅ 已更新 {skill_name} 分数为 {new_score}")
        else:
            print(f"❌ 技能 {skill_name} 不存在")
    
    def add_learning_resource(self, skill_name: str, resource: str):
        """添加学习资源"""
        if skill_name in self.skills:
            self.skills[skill_name].learning_resources.append(resource)
            self.save_data()
            print(f"✅ 已为 {skill_name} 添加学习资源: {resource}")
    
    def add_practice_project(self, skill_name: str, project: str):
        """添加实践项目"""
        if skill_name in self.skills:
            self.skills[skill_name].practice_projects.append(project)
            self.save_data()
            print(f"✅ 已为 {skill_name} 添加实践项目: {project}")
    
    def update_project_progress(self, project_name: str, completion: int, 
                              achievements: List[str] = None, 
                              challenges: List[str] = None):
        """更新项目进度"""
        if project_name in self.projects:
            self.projects[project_name].completion_percentage = completion
            if achievements:
                self.projects[project_name].key_achievements.extend(achievements)
            if challenges:
                self.projects[project_name].technical_challenges.extend(challenges)
            self.save_data()
            print(f"✅ 已更新项目 {project_name} 进度为 {completion}%")
    
    def get_skill_level(self, score: int) -> SkillLevel:
        """根据分数判断技能等级"""
        if score >= 90:
            return SkillLevel.EXPERT
        elif score >= 80:
            return SkillLevel.PROFICIENT
        elif score >= 70:
            return SkillLevel.INTERMEDIATE
        else:
            return SkillLevel.BEGINNER
    
    def get_phase_progress(self) -> Dict[str, Dict]:
        """获取各阶段学习进度"""
        foundation_skills = ["Python高级特性", "PyTorch深度学习", "大模型API集成", "LangChain框架", "向量数据库"]
        core_skills = ["多Agent系统架构", "强化学习算法", "RLHF实现", "分布式系统设计", "模型部署优化", "AI安全防护"]
        expert_skills = ["神经符号融合", "具身智能", "大规模系统架构", "技术团队管理", "创新研究能力"]
        
        phases = {
            "基础建设期": foundation_skills,
            "核心技能期": core_skills,
            "专家精进期": expert_skills
        }
        
        progress = {}
        for phase_name, skill_list in phases.items():
            total_score = 0
            total_target = 0
            completed_skills = 0
            
            for skill_name in skill_list:
                if skill_name in self.skills:
                    skill = self.skills[skill_name]
                    total_score += skill.current_score
                    total_target += skill.target_score
                    if skill.current_score >= skill.target_score:
                        completed_skills += 1
            
            avg_progress = (total_score / total_target * 100) if total_target > 0 else 0
            completion_rate = (completed_skills / len(skill_list) * 100) if skill_list else 0
            
            progress[phase_name] = {
                "平均进度": f"{avg_progress:.1f}%",
                "完成技能数": f"{completed_skills}/{len(skill_list)}",
                "完成率": f"{completion_rate:.1f}%",
                "状态": "已完成" if completion_rate >= 80 else "进行中" if completion_rate > 0 else "未开始"
            }
        
        return progress
    
    def generate_progress_report(self) -> str:
        """生成进度报告"""
        report = []
        report.append("🎯 AI Agent技能掌握进度报告")
        report.append("=" * 50)
        
        # 阶段进度
        report.append("\n📊 学习阶段进度:")
        phase_progress = self.get_phase_progress()
        for phase, data in phase_progress.items():
            report.append(f"\n{phase}:")
            for key, value in data.items():
                report.append(f"  {key}: {value}")
        
        # 技能详情
        report.append("\n📚 技能掌握详情:")
        categories = {}
        for skill in self.skills.values():
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill)
        
        for category, skills in categories.items():
            report.append(f"\n{category}:")
            for skill in skills:
                level = self.get_skill_level(skill.current_score)
                progress = f"{skill.current_score}/{skill.target_score}"
                status = "✅" if skill.current_score >= skill.target_score else "🔄"
                report.append(f"  {status} {skill.skill_name}: {progress} ({level.value})")
        
        # 项目进度
        if self.projects:
            report.append("\n🛠️ 项目进度:")
            for project in self.projects.values():
                status = "✅" if project.completion_percentage >= 100 else "🔄"
                report.append(f"  {status} {project.project_name}: {project.completion_percentage}%")
        
        # 学习建议
        report.append("\n💡 学习建议:")
        low_score_skills = [skill for skill in self.skills.values() if skill.current_score < skill.target_score]
        if low_score_skills:
            # 按分数差距排序
            low_score_skills.sort(key=lambda x: x.target_score - x.current_score, reverse=True)
            report.append("  优先提升以下技能:")
            for skill in low_score_skills[:3]:
                gap = skill.target_score - skill.current_score
                report.append(f"    • {skill.skill_name} (差距: {gap}分)")
        
        return "\n".join(report)
    
    def get_next_milestones(self) -> List[str]:
        """获取下一步里程碑"""
        milestones = []
        
        # 找出最需要提升的技能
        skills_to_improve = []
        for skill in self.skills.values():
            if skill.current_score < skill.target_score:
                gap = skill.target_score - skill.current_score
                skills_to_improve.append((skill.skill_name, gap))
        
        skills_to_improve.sort(key=lambda x: x[1], reverse=True)
        
        if skills_to_improve:
            milestones.append(f"🎯 重点提升: {skills_to_improve[0][0]}")
            milestones.append(f"📚 建议学习时间: 每天2-3小时")
            milestones.append(f"🛠️ 实践项目: 选择相关项目进行练习")
        
        return milestones

def main():
    """主函数 - 演示使用"""
    tracker = SkillTracker()
    
    print("🚀 AI Agent技能追踪系统")
    print("=" * 40)
    
    # 显示当前进度
    print(tracker.generate_progress_report())
    
    # 显示下一步建议
    print("\n🎯 下一步行动建议:")
    milestones = tracker.get_next_milestones()
    for milestone in milestones:
        print(f"  {milestone}")
    
    print("\n" + "=" * 40)
    print("💡 使用说明:")
    print("1. 使用 update_skill_score() 更新技能分数")
    print("2. 使用 add_learning_resource() 添加学习资源")
    print("3. 使用 add_practice_project() 记录实践项目")
    print("4. 定期运行生成进度报告")

if __name__ == "__main__":
    main()