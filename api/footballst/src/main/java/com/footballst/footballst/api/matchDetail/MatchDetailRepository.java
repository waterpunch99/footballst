package com.footballst.footballst.api.matchDetail;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface MatchDetailRepository extends JpaRepository<MatchDetail, Long> {
    List<MatchDetail> findByMatchId(Long matchId);
}
