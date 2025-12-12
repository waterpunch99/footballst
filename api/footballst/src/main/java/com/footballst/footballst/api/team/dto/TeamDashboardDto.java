package com.footballst.footballst.api.team.dto;

import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class TeamDashboardDto {

    private Long teamId;
    private Integer season;

    private Summary summary;
    private Recent5 recent5;
    private Performance performance;

    @Getter
    @Builder
    public static class Summary {
        private Integer totalMatches;
        private Integer wins;
        private Integer draws;
        private Integer losses;
        private Integer goalsFor;
        private Integer goalsAgainst;
        private Integer goalDiff;
        private Double winRate;
    }

    @Getter
    @Builder
    public static class Recent5 {
        private Double recent5WinRate;
        private Double recent5GoalDiff;
    }

    @Getter
    @Builder
    public static class Performance {
        private Double goalsPerMatch;
        private Double goalsConcededPerMatch;
        private Double goalDiffPerMatch;
    }
}

