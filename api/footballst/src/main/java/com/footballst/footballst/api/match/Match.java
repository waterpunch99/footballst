package com.footballst.footballst.api.match;
import com.footballst.footballst.api.team.Team;
import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDateTime;

@Getter
@Entity
@Table(name = "matches")
public class Match {

    @Id
    @Column(name = "match_id")
    private Long id;

    private LocalDateTime matchDate;

    @Column(name = "home_team_id")
    private Long homeTeamId;

    @Column(name = "away_team_id")
    private Long awayTeamId;


    private Integer homeGoals;
    private Integer awayGoals;
}

