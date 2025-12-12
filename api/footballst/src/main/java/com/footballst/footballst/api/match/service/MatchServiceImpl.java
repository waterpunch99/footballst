package com.footballst.footballst.api.match.service;

import com.footballst.footballst.api.event.EventRepository;
import com.footballst.footballst.api.event.dto.EventResponseDto;
import com.footballst.footballst.api.match.Match;
import com.footballst.footballst.api.match.MatchRepository;
import com.footballst.footballst.api.match.dto.MatchFullResponseDto;
import com.footballst.footballst.api.match.dto.TeamSummaryDto;
import com.footballst.footballst.api.matchDetail.MatchDetail;
import com.footballst.footballst.api.matchDetail.MatchDetailRepository;
import com.footballst.footballst.api.team.Team;
import com.footballst.footballst.api.team.TeamRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
@RequiredArgsConstructor
public class MatchServiceImpl implements MatchService {

    private final MatchRepository matchRepository;
    private final MatchDetailRepository matchDetailRepository;
    private final EventRepository eventRepository;
    private final TeamRepository teamRepository;

    @Override
    public List<Match> getAllMatches() {
        return matchRepository.findAll();
    }

    @Override
    public MatchFullResponseDto getMatchFull(Long matchId) {

        Match match = matchRepository.findById(matchId)
                .orElseThrow(() -> new EntityNotFoundException("경기 없음"));

        MatchDetail detail = matchDetailRepository.findById(matchId)
                .orElseThrow(() -> new EntityNotFoundException("경기 상세 없음"));

        Team home = teamRepository.findById(match.getHomeTeamId())
                .orElseThrow(() -> new EntityNotFoundException("홈팀 정보 없음"));

        Team away = teamRepository.findById(match.getAwayTeamId())
                .orElseThrow(() -> new EntityNotFoundException("어웨이팀 정보 없음"));

        List<EventResponseDto> events = eventRepository.findByMatchId(matchId)
                .stream()
                .map(EventResponseDto::fromEntity)
                .toList();

        return MatchFullResponseDto.builder()
                .matchId(match.getId())
                .date(detail.getDate())
                .homeTeam(
                        TeamSummaryDto.builder()
                                .teamId(home.getTeamId())
                                .name(home.getName())
                                .logo(home.getLogo())
                                .build()
                )
                .awayTeam(
                        TeamSummaryDto.builder()
                                .teamId(away.getTeamId())
                                .name(away.getName())
                                .logo(away.getLogo())
                                .build()
                )
                .homeGoals(match.getHomeGoals())
                .awayGoals(match.getAwayGoals())
                .events(events)
                .build();
    }
}

