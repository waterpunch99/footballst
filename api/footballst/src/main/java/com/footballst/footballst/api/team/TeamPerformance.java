package com.footballst.footballst.api.team;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Entity
@Table(name = "team_performance")
@Getter
public class TeamPerformance {

    @EmbeddedId
    private TeamPerformanceId id;

    @Column(name = "goal_diff_per_match")
    private Double goalDiffPerMatch;

    @Column(name = "goals_per_match")
    private Double goalsPerMatch;

    @Column(name = "goals_conceded_per_match")
    private Double goalsConcededPerMatch;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
}

