with
    plays as (
        select (
            case
            when result = 'd' then opp
            when result = 'w'
                then (
                    select item from actions
                    where wins_against = opp
                )
            when result = 'l'
                then (
                    select wins_against from actions
                    where item = opp
                )
            end
        ) as action,
        result
        from strategy
    ),
    scores as (
        select actions.score + (
            case 
                when plays.result = 'w' then 6
                when plays.result = 'd' then 3
                else 0
            end
        ) as score,
        *
        from plays, actions
        where plays.action = actions.item
    )
select sum(score) from scores

