package com.footballst.footballst.api.event;
import com.footballst.footballst.api.match.Match;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Entity
@Table(name = "events")
@Getter
@NoArgsConstructor
public class Event {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "match_id")
    private Long matchId;


    private Integer elapsed;

    @Column(name = "team_id")
    private Integer teamId;

    @Column(name = "player_id")
    private String playerId;

    @Column(name = "player_name")
    private String playerName;

    @Column(name = "assist_id")
    private Long assistId;

    @Column(name = "assist_name")
    private String assistName;

    private String type;

    private String detail;
}
