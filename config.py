class SafetyThresholds:
    def __init__(self):
        self._safe_speed = 3.2  # 默认安全速度
        self._gas_concentration_limit = 1.0

    @property
    def speed_green(self):
        """绿色区间阈值：安全速度的78%"""
        return round(0.78 * self._safe_speed, 1)

    @property
    def speed_yellow(self):
        """黄色区间阈值：安全速度的100%"""
        return self._safe_speed

    @property
    def gas_concentration(self):
        """瓦斯浓度阈值（固定值）"""
        return self._gas_concentration_limit

    def update_safe_speed(self, new_speed: float):
        """更新安全速度阈值"""
        self._safe_speed = round(new_speed, 1)

# 全局阈值配置实例
SAFETY_THRESHOLDS = SafetyThresholds()