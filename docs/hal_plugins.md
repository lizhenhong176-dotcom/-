# HAL 插件说明

HAL 的五个核心分析插件及其在木马检测中的用途。

## 1. Dataflow Plugin
**用途**: 数据流方向分析
- 确定门之间的数据流向 (forward/backward)
- 追踪数据路径
- 找到所有数据终点 (sinks)

**木马检测应用**:
- 追踪敏感信号 (密钥、配置寄存器) 的数据流
- 检测数据是否流向了非预期的输出
- 发现隐藏的数据旁路

## 2. FSM Plugin
**用途**: 有限状态机提取与分析
- 从门级网表自动提取 FSM
- 分析状态可达性
- 检测死态和不可达状态

**木马检测应用**:
- 检测 FSM 中的额外隐藏状态 (木马触发状态)
- 发现 rare-trigger 条件 (极低概率触发的状态转换)
- 验证状态机完整性

## 3. Graph Algorithm Plugin
**用途**: 通用图算法
- 连通分量分析
- 环路检测
- 最短路径
- 子图匹配

**木马检测应用**:
- 检测已知木马结构的子图匹配
- 发现异常的反馈环路
- 计算信号影响力路径

## 4. Simulator Plugin
**用途**: 门级仿真
- 测试向量注入
- 波形追踪
- 覆盖率分析

**木马检测应用**:
- 找到仿真中从未翻转的门 (可能隐藏在 rare-trigger 条件下)
- 验证可疑路径是否真的可激活
- 随机测试向量 + 覆盖率缺口分析

## 5. Boolean Influence Plugin
**用途**: 布尔影响力分析
- 量化每个输入对输出的布尔影响力
- 识别关键控制信号

**木马检测应用**:
- 检测是否有异常信号对关键输出有不正常的影响
- 与参考设计的影响力对比，发现篡改
- 识别隐蔽的触发输入

## 插件加载

```python
from hal.plugin_manager import PluginManager

pm = PluginManager()
pm.load_all()

# 使用
df = pm.dataflow
fsm_plugin = pm.fsm
graph = pm.graph_algorithm
sim = pm.simulator
influence = pm.boolean_influence
```
