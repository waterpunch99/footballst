package com.footballst.footballst.api.match.service;

import com.footballst.footballst.api.match.Match;
import com.footballst.footballst.api.match.MatchRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
@RequiredArgsConstructor
@Service
public class MatchServiceImpl implements MatchService {
    private final MatchRepository matchRepository;
    @Override
    public List<Match> getAllMatches() {
        return matchRepository.findAll();
    }
}
