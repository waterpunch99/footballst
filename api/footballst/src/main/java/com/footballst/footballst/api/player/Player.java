package com.footballst.footballst.api.player;
import com.footballst.footballst.api.team.Team;
import jakarta.persistence.*;
import lombok.Getter;

import static jakarta.persistence.FetchType.LAZY;

@Getter
@Entity
@Table(name = "players")
public class Player {

    @Id
    @Column(name = "player_id")
    private String id;


    @Column(name = "team_id")
    private Long teamId;


    private String name;
    private String age;
    private String number;
    private String position;
    private String photo;
}

