from django.db.models import Q

from apps.base.models import QuotaRule
from apps.bot_mgmt.models import Bot
from apps.knowledge_mgmt.models import FileKnowledge
from apps.model_provider_mgmt.models import LLMSkill


def get_quota_client(request):
    teams = request.user.group_list
    current_team = request.COOKIES.get("current_team")
    if not current_team:
        current_team = teams[0]
    client = QuotaUtils(request.user.username, current_team)
    return client


class QuotaUtils(object):
    def __init__(self, username, team):
        self.username = username
        self.team = team
        self.quota_list = self.get_quota_list()

    def get_quota_list(self):
        quota_list = QuotaRule.objects.filter(
            Q(target_type="user", target_list__contains=self.username)
            | Q(target_type="team", target_list__contains=self.team)
        ).values()
        return list(quota_list)

    def get_file_quota(self):
        unit_map = {"GB": 1024, "MB": 1}
        file_size_map = {"shared": [], "private": []}
        type_map = {"shared": "shared", "uniform": "private"}
        if not self.quota_list:
            return -1, 0, False
        for quota in self.quota_list:
            file_size_map[type_map[quota["rule_type"]]].append(quota["file_size"] * unit_map[quota["unit"]])
        if file_size_map["private"]:
            file_size_list = file_size_map["private"]
            file_list = FileKnowledge.objects.filter(knowledge_document__created_by=self.username)
        else:
            file_size_list = file_size_map["shared"]
            file_list = FileKnowledge.objects.filter(knowledge_document__knowledge_base__team=self.team)
        used_file_size_list = [i.file.size for i in file_list if i.file] + [0]
        used_file_size = sum(used_file_size_list)
        return (
            min(file_size_list) if file_size_list else 0,
            round(used_file_size, 2),
            bool(file_size_map["private"]),
        )

    def get_skill_quota(self):
        skill_count_map = {"shared": [], "private": []}
        type_map = {"shared": "shared", "uniform": "private"}
        if not self.quota_list:
            return -1, 0, False
        for quota in self.quota_list:
            skill_count_map[type_map[quota["rule_type"]]].append(quota["skill_count"])
        if skill_count_map["private"]:
            skill_count_list = skill_count_map["private"]
            skill_count = LLMSkill.objects.filter(created_by=self.username).count()
        else:
            skill_count_list = skill_count_map["shared"]
            skill_count = LLMSkill.objects.filter(team__contains=self.team).count()

        return (
            min(skill_count_list) if skill_count_list else 0,
            skill_count,
            bool(skill_count_map["private"]),
        )

    def get_bot_quota(self):
        bot_count_map = {"shared": [], "private": []}
        type_map = {"shared": "shared", "uniform": "private"}
        if not self.quota_list:
            return -1, 0, False
        for quota in self.quota_list:
            bot_count_map[type_map[quota["rule_type"]]].append(quota["bot_count"])
        if bot_count_map["private"]:
            bot_count_list = bot_count_map["private"]
            bot_count = Bot.objects.filter(created_by=self.username).count()
        else:
            bot_count_list = bot_count_map["shared"]
            bot_count = Bot.objects.filter(team__contains=self.team).count()
        return (
            min(bot_count_list) if bot_count_list else 0,
            bot_count,
            bool(bot_count_map["private"]),
        )
