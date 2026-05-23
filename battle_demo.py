"""MAgent2 Battle 环境演示脚本

两队智能体（红队 red vs 蓝队 blue）在 45x45 网格上进行团战。
使用随机策略运行，输出每步的存活数量和最终结果。
"""

from magent2.environments import battle_v4


def run_battle_demo():
    # 创建环境 (AEC 模式，即逐个智能体轮流行动)
    env = battle_v4.env(map_size=45, max_cycles=300)
    env.reset()

    red_alive = 0
    blue_alive = 0
    step_count = 0

    # 统计初始数量
    for agent in env.agents:
        if agent.startswith("red"):
            red_alive += 1
        else:
            blue_alive += 1
    print(f"=== MAgent2 Battle Demo ===")
    print(f"Initial: red={red_alive}, blue={blue_alive}, total={red_alive + blue_alive}")
    print()

    # 主循环：逐个智能体行动
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None  # 已死亡或截断的智能体不行动
        else:
            # 随机选择一个合法动作
            action = env.action_space(agent).sample()

        env.step(action)
        step_count += 1

        # 每 1000 步打印一次状态
        if step_count % 1000 == 0:
            red = sum(1 for a in env.agents if a.startswith("red"))
            blue = sum(1 for a in env.agents if a.startswith("blue"))
            print(f"  step {step_count:>6d}: red={red:>3d}, blue={blue:>3d}")

    # 最终结果
    red_final = sum(1 for a in env.agents if a.startswith("red"))
    blue_final = sum(1 for a in env.agents if a.startswith("blue"))
    print()
    print(f"=== Battle Finished ===")
    print(f"Total steps: {step_count}")
    print(f"Survivors: red={red_final}, blue={blue_final}")
    if red_final > blue_final:
        print("Result: Red team wins!")
    elif blue_final > red_final:
        print("Result: Blue team wins!")
    else:
        print("Result: Draw!")

    env.close()


if __name__ == "__main__":
    run_battle_demo()
