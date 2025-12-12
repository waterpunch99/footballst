package com.footballst.footballst.api.team;


import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "team_stats")
@Getter
public class TeamStats {

    @EmbeddedId
    private TeamStatsId id;


    @Column(name = "total_matches")
    private Integer totalMatches;

    @Column(name = "wins")
    private Integer wins;

    @Column(name = "draws")
    private Integer draws;

    @Column(name = "losses")
    private Integer losses;

    @Column(name = "goals_for")
    private Integer goalsFor;

    @Column(name = "goals_against")
    private Integer goalsAgainst;

    @Column(name = "goal_diff")
    private Integer goalDiff;

    @Column(name = "win_rate")
    private Double winRate;

    @Column(name = "recent5_win_rate")
    private Double recent5WinRate;

    @Column(name = "recent5_goal_diff")
    private Double recent5GoalDiff;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}

