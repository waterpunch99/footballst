package com.footballst.footballst.api.match.dto;

import com.footballst.footballst.api.match.Match;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
@Getter
@Builder
public class MatchResponseDto {

    private Long matchId;
    private LocalDateTime matchDate;

    private Long homeTeamId;
    private String homeTeamName;

    private Long awayTeamId;
    private String awayTeamName;

    private Integer homeGoals;
    private Integer awayGoals;

    public static MatchResponseDto fromEntity(Match match) {
        return MatchResponseDto.builder()
                .matchId(match.getId())
                .matchDate(match.getMatchDate())
                .homeTeamId(match.getHomeTeamId())     // 변경
                .awayTeamId(match.getAwayTeamId())
                .homeGoals(match.getHomeGoals())
                .awayGoals(match.getAwayGoals())
                .build();
    }
}


