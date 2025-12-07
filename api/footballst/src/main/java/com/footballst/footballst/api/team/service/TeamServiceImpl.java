package com.footballst.footballst.api.team.service;
import com.footballst.footballst.api.team.TeamRepository;
import com.footballst.footballst.api.team.dto.TeamResponseDto;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class TeamServiceImpl implements TeamService {

    private final TeamRepository teamRepository;
    @Override
    public List<TeamResponseDto> getAllTeams() {
        return teamRepository.findAll()
                .stream()
                .map(TeamResponseDto::fromEntity)
                .toList();
    }
}
