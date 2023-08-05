#include "GamesServices.h"
#include "GamesServicesImpl.h"

GamesServices::GamesServices()
	: m_gamesServicesImpl(new GamesServicesImpl())
{
	LOG("GamesServices()");
}
GamesServices::~GamesServices()
{
	LOG("~GamesServices()");
}

void GamesServices::init()
{
	m_gamesServicesImpl->Init();
}

void GamesServices::release()
{
	m_gamesServicesImpl->Release();
}

void GamesServices::signIn()
{
	m_gamesServicesImpl->SignIn();
}

void GamesServices::signOut()
{
	m_gamesServicesImpl->SignOut();
}

bool GamesServices::isSignedIn()
{
	return m_gamesServicesImpl->IsSignedIn();
}

void GamesServices::showLeaderboard(const char* id)
{
	m_gamesServicesImpl->ShowLeaderboard(id);
}

void GamesServices::submitScoreLeaderboard(const char* id, uint16_t value)
{
	m_gamesServicesImpl->SubmitScoreLeaderboard(id, value);
}

void GamesServices::showAchievement()
{
	m_gamesServicesImpl->ShowAchievement();
}

void GamesServices::unlockAchievement(const char* id)
{
	m_gamesServicesImpl->UnlockAchievement(id);
}

void GamesServices::incrementAchievement(const char* id, uint16_t value)
{
	m_gamesServicesImpl->IncrementAchievement(id, value);
}
