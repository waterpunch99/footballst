package com.footballst.footballst.api.team;
import jakarta.persistence.*;
import lombok.Getter;

@Getter
@Entity
@Table(name = "teams")
public class Team {

    @Id
    @Column(name = "team_id")
    private Long teamId;
    private String name;
    private String country;
    private Integer leagueId;
    private String logo;
}
