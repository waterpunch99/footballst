package com.footballst.footballst.api.team;

import com.footballst.footballst.api.team.TeamStats;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface TeamStatsRepository extends JpaRepository<TeamStats, TeamStatsId> {
    Optional<TeamStats> findByIdTeamIdAndIdSeason(Long teamId, Integer season);

}
