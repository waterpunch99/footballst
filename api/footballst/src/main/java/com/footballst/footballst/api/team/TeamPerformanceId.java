package com.footballst.footballst.api.team;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Embeddable
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class TeamPerformanceId implements Serializable {

    @Column(name = "team_id")
    private Long teamId;

    @Column(name = "season")
    private Integer season;
}

