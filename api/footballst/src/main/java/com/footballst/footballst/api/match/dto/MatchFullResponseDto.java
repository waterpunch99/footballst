package com.footballst.footballst.api.match.dto;

import com.footballst.footballst.api.event.dto.EventResponseDto;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Builder
public class MatchFullResponseDto {

    private Long matchId;
    private LocalDateTime date;

    private TeamSummaryDto homeTeam;
    private TeamSummaryDto awayTeam;

    private Integer homeGoals;
    private Integer awayGoals;

    private List<EventResponseDto> events;
}
