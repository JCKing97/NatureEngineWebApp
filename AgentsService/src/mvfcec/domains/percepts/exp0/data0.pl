/* 
Percept Example for the "Standing Discriminator" strategy players
Date: 20 Nov 2018
*/

:- dynamic agents/2.

agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 0).
agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 1).
agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 2).
agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),3).
agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4).
agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),5).

% agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1) "defect"s against agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),3), and  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2) observes this
% agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1) will have a bad "Standing Discriminator" from  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2)'s viewing after this
observed_at(did(agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1),  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2), agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),3), "defect"), 1).
%  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2) spreads "negative" gossip about agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1)
% ["Distrusting"] agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4) will not be affected by this
% Trusting agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),0) will give agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1) in a bad "Standing Discriminator"
observed_at(said( agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2), agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), "negative"), 2).
observed_at(said( agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 0), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), "negative"), 2).
% agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1) "cooperate"s will agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),5), with agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4) observing this
% this will mean that the good "Standing Discriminator" of agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1) in agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4)'s eyes persists
observed_at(did(agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4), agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),5), "cooperate"), 3).
% agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1) has a bad "Standing Discriminator" with  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2)
% agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1) attempts to spread "negative" gossip about agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),0)
% This will not affect the "Standing Discriminator" of agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),0) in  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2)'s eyes
% This is because agent("desc",2) holds agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1) in bad "Standing Discriminator"
observed_at(said(agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1),  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 0), "negative"), 3).
% agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4) sreads "positive" gossip about agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1)
% agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),0) will restore the good "Standing Discriminator" of agent(strategy("Standing Discriminator", "desc", ["trusting"])agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), 1) in it's eyes
observed_at(said(agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 0), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), "positive"), 4).
% Agent 2 is trusting and is told by Agent 4 that Agent 1 is good so restores it's goos "Standing Discriminator"
observed_at(said(agent(strategy("Standing Discriminator", "desc", ["distrusting"]), community(0), generation(community(0), 0),4), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1), "positive"), 4).
% agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1) now has a restored good "Standing Discriminator" with  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2)
% agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1) spreads "negative" gossip about agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),0)
% This will affect the "Standing Discriminator" of agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),0) in  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2)'s eyes
observed_at(said(agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),1),  agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0),2), agent(strategy("Standing Discriminator", "desc", ["trusting"]), community(0), generation(community(0), 0), 0), "negative"), 5).