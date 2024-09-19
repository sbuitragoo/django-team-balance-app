import random
from collections import defaultdict

class Player:
    def __init__(self, id, name, skill_rate, preferred_position, secondary_position):
        self.id = id
        self.name = name
        self.skill_rate = skill_rate
        self.preferred_position = preferred_position
        self.secondary_position = secondary_position

    def __repr__(self):
        return f'{self.name} ({self.skill_rate}) - {self.preferred_position}/{self.secondary_position}'

class Assigner:

    @staticmethod
    def assign_randomly(positions, position, team1, team2, total_skill_team1, total_skill_team2, max_team_size):
        pos_players = sorted(positions[position], key=lambda x: -x.skill_rate)
        for player in pos_players:
            # Randomly decide whether to assign the player to team1 or team2 while trying to balance skill rates
            if len(team1) < max_team_size and len(team2) < max_team_size:
                if total_skill_team1 < total_skill_team2:
                    team1.append(player)
                    total_skill_team1 += player.skill_rate
                elif total_skill_team2 < total_skill_team1:
                    team2.append(player)
                    total_skill_team2 += player.skill_rate
                else:  # Random choice if both teams have equal skill
                    if random.choice([True, False]):
                        team1.append(player)
                        total_skill_team1 += player.skill_rate
                    else:
                        team2.append(player)
                        total_skill_team2 += player.skill_rate
            elif len(team1) < max_team_size:
                team1.append(player)
                total_skill_team1 += player.skill_rate
            else:
                team2.append(player)
                total_skill_team2 += player.skill_rate

        return total_skill_team1, total_skill_team2

    @staticmethod
    def swap_stronger_player(team_with_gk, team_without_gk):
        # Find and swap the strongest player from the team without the goalkeeper
        team_without_gk.sort(key=lambda x: -x.skill_rate)
        if team_without_gk:
            player_to_swap = team_without_gk[0]
            team_with_gk.append(player_to_swap)
            team_without_gk.remove(player_to_swap)

    @staticmethod
    def balance_goalkeepers_and_skills(team1, team2, total_skill_team1, total_skill_team2):
        # Check for goalkeepers
        team1_has_gk = any(player.preferred_position == "goalkeeper" for player in team1)
        team2_has_gk = any(player.preferred_position == "goalkeeper" for player in team2)

        # Swap players if needed to balance skill if one team has a goalkeeper and the other doesn't
        if team1_has_gk and not team2_has_gk and total_skill_team1 > total_skill_team2:
            Assigner.swap_stronger_player(team1, team2)
        elif team2_has_gk and not team1_has_gk and total_skill_team2 > total_skill_team1:
            Assigner.swap_stronger_player(team2, team1)

    @staticmethod
    def balance_teams(players):
        # Shuffle players randomly to ensure some fairness
        random.shuffle(players)
        
        # Divide players by preferred positions
        positions = defaultdict(list)
        for player in players:
            positions[player.preferred_position].append(player)

        print("Positions: ", positions)
        
        # Initialize teams
        team1, team2 = [], []
        total_skill_team1, total_skill_team2 = 0, 0
        max_team_size = len(players) // 2

        # Assign players to teams by positions with slight randomization
        for position in ["goalkeeper", "defender", "midfielder", "attacker"]:
            total_skill_team1, total_skill_team2 = Assigner.assign_randomly(
                positions, position, team1, team2, total_skill_team1, total_skill_team2, max_team_size
            )

        print(total_skill_team1, total_skill_team2)

        # If teams are uneven, move players until balanced
        while len(team1) > len(team2):
            team2.append(team1.pop())
        while len(team2) > len(team1):
            team1.append(team2.pop())

        print(team1,team2)

        # Ensure balance based on goalkeeper and skill rate
        Assigner.balance_goalkeepers_and_skills(team1, team2, total_skill_team1, total_skill_team2)
        
        return team1, team2

# if __name__ == "__main__":

#     # Example usage
#     players = [
#         Player(1,'Santiago', 4.5, 'attacker', 'midfielder'),
#         Player(1,'Juan Pablo', 4.5, 'attacker', 'midfielder'),
#         Player(1,'Sebas', 4.0, 'defender', 'midfielder'),
#         # Player('Emilio', 3.0, 'defender', 'midfielder'),
#         Player(1,'Daniel Montes', 4.5, 'attacker', 'defender'),
#         Player(1,'Daniel Mejia', 4.0, 'attacker', 'defender'),
#         Player(1,'Julian G', 4.5, 'defender', 'midfielder'),
#         Player(1,'Geiber A', 4.5, 'attacker', 'midfielder'),
#         Player(1,'Stiven', 4.6, 'attacker', 'midfielder'),
#         # Player('Camilo P', 2.5, 'defender', 'midfielder'),
#         Player(1,'Rafael', 4.5, 'attacker', 'midfielder'),
#         Player(1,'Alejo', 4.0, 'goalkeeper', 'defender')
#     ]

#     team1, team2 = balance_teams(players)

#     # Print teams and total skill for verification
#     def print_team_info(team, team_name):
#         total_skill = sum(player.skill_rate for player in team)
#         print(f"{team_name}:")
#         for player in team:
#             print(player)
#         print(f"Total Skill: {total_skill}\n")
    
#     print(type(team1[0]))

#     print_team_info(team1, "Team 1")
#     print_team_info(team2, "Team 2")