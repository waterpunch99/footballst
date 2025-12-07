package com.footballst.footballst.api.event.dto;
import com.footballst.footballst.api.event.Event;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class EventResponseDto {

    private Long matchId;
    private Integer elapsed;
    private Integer teamId;
    private String playerId;
    private String playerName;
    private Long assistId;
    private String assistName;
    private String type;
    private String detail;

    public static EventResponseDto fromEntity(Event e) {
        return EventResponseDto.builder()
                .matchId(e.getMatchId())
                .elapsed(e.getElapsed())
                .teamId(e.getTeamId())
                .playerId(e.getPlayerId())
                .playerName(e.getPlayerName())
                .assistId(e.getAssistId())
                .assistName(e.getAssistName())
                .type(e.getType())
                .detail(e.getDetail())
                .build();
    }
}
