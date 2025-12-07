package com.footballst.footballst.api.team.dto;
import com.footballst.footballst.api.team.Team;
import lombok.Builder;
import lombok.Getter;

@Getter
@Builder
public class TeamResponseDto {

    private Long teamId;
    private String name;
    private String country;
    private Integer leagueId;
    private String logo;

    public static TeamResponseDto fromEntity(Team team) {
        return TeamResponseDto.builder()
                .teamId(team.getTeamId())
                .name(team.getName())
                .country(team.getCountry())
                .leagueId(team.getLeagueId())
                .logo(team.getLogo())
                .build();
    }
}
