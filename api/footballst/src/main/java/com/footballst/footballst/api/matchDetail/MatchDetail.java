package com.footballst.footballst.api.matchDetail;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "fixture_details")
@Getter
@NoArgsConstructor
public class MatchDetail {

    @Id
    @Column(name = "match_id")
    private Integer matchId;

    private String referee;

    private String venue;

    private String timezone;

    private LocalDateTime date;
}

