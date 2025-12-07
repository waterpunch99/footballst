package com.footballst.footballst.api.matchDetail.service;

import com.footballst.footballst.api.matchDetail.MatchDetail;
import com.footballst.footballst.api.matchDetail.MatchDetailRepository;
import com.footballst.footballst.api.matchDetail.dto.MatchDetailResponseDto;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class MatchDetailServiceImpl implements MatchDetailService {

    private final MatchDetailRepository matchDetailRepository;

    @Override
    public MatchDetailResponseDto getMatchDetail(Long matchId) {
        MatchDetail detail = matchDetailRepository.findById(matchId)
                .orElseThrow(() -> new EntityNotFoundException("해당 경기 상세 없음"));

        return MatchDetailResponseDto.fromEntity(detail);
    }
}



