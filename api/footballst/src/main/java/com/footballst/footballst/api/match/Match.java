package com.footballst.footballst.api.match;

import jakarta.persistence.*;
import lombok.Data;
@Data
@Entity
@Table(name = "matches")
public class Match {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String matchDate;
    private String homeTeam;
    private String awayTeam;
    private Integer homeGoals;
    private Integer awayGoals;
}
