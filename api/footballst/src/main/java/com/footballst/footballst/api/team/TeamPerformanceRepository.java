package com.footballst.footballst.api.team;


import com.footballst.footballst.api.team.TeamPerformance;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface TeamPerformanceRepository extends JpaRepository<TeamPerformance, TeamPerformanceId> {

    Optional<TeamPerformance> findByIdTeamIdAndIdSeason(Long teamId, Integer season);
}

