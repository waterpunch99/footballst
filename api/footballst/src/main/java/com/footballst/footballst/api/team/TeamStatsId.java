package com.footballst.footballst.api.team;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Embeddable
@Getter
@NoArgsConstructor
@EqualsAndHashCode
public class TeamStatsId implements Serializable {
    @Column(name = "team_id")
    private Long teamId;

    @Column(name = "season")
    private Integer season;

    public TeamStatsId(Long teamId, Integer season) {
        this.teamId = teamId;
        this.season = season;
    }
}
