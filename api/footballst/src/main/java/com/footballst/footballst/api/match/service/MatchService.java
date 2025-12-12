package com.footballst.footballst.api.match.service;

import com.footballst.footballst.api.match.Match;
import com.footballst.footballst.api.match.dto.MatchFullResponseDto;

import java.util.List;

public interface MatchService {
    List<Match> getAllMatches();
    MatchFullResponseDto getMatchFull(Long matchId);
}
