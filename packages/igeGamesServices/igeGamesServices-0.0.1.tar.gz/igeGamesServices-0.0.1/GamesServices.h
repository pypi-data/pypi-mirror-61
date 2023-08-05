#pragma once

#include <stdint.h>

#ifdef _WIN32
#define IGE_EXPORT __declspec(dllexport)
#else
#define IGE_EXPORT
#endif

#ifdef NDEBUG
	#define LOG_VERBOSE(...)
	#define LOG_DEBUG(...)
	#define LOG(...)
	#define LOG_WARN(...)
	#define LOG_ERROR(...)
#else
	#if defined(__ANDROID__)
		#include <android/log.h>

		#define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "Social", __VA_ARGS__);
		#define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "Social", __VA_ARGS__);
		#define LOG(...) __android_log_print(ANDROID_LOG_INFO, "Social", __VA_ARGS__);
		#define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "Social", __VA_ARGS__);
		#define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "Social", __VA_ARGS__);
	#else
		void GamesServicesLogMessage(const char* format, ...);

		#define LOG_VERBOSE(...) GamesServicesLogMessage(__VA_ARGS__);
		#define LOG_DEBUG(...) GamesServicesLogMessage(__VA_ARGS__);
		#define LOG(...) GamesServicesLogMessage(__VA_ARGS__);
		#define LOG_WARN(...) GamesServicesLogMessage(__VA_ARGS__);
		#define LOG_ERROR(...) GamesServicesLogMessage(__VA_ARGS__);
	#endif
#endif

class GamesServicesImpl;
class IGE_EXPORT GamesServices
{
public:
	GamesServices();
	~GamesServices();
	void init();
	void release();
	void signIn();
	void signOut();
	bool isSignedIn();
	void showLeaderboard(const char* id);
	void submitScoreLeaderboard(const char* id, uint16_t value);
	void showAchievement();
	void unlockAchievement(const char* id);
	void incrementAchievement(const char* id, uint16_t value);

private:
	GamesServicesImpl* m_gamesServicesImpl;
};
