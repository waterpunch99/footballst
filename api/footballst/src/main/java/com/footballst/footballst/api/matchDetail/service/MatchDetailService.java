package com.footballst.footballst.api.matchDetail.service;

import com.footballst.footballst.api.matchDetail.dto.MatchDetailResponseDto;

public interface MatchDetailService {
    MatchDetailResponseDto getMatchDetail(Long matchId);
}


