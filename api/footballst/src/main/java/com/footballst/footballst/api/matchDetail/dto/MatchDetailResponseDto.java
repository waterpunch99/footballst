package com.footballst.footballst.api.matchDetail.dto;

import com.footballst.footballst.api.matchDetail.MatchDetail;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Builder
public class MatchDetailResponseDto {

    private Integer matchId;
    private String referee;
    private String venue;
    private String timezone;
    private LocalDateTime date;

    public static MatchDetailResponseDto fromEntity(MatchDetail detail) {
        return MatchDetailResponseDto.builder()
                .matchId(detail.getMatchId())
                .referee(detail.getReferee())
                .venue(detail.getVenue())
                .timezone(detail.getTimezone())
                .date(detail.getDate())
                .build();
    }
}

