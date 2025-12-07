package com.footballst.footballst.api.team.service;

import com.footballst.footballst.api.team.dto.TeamResponseDto;

import java.util.List;

public interface TeamService {
    List<TeamResponseDto> getAllTeams();

}
