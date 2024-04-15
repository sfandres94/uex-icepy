module QuizGame
{
    sequence<string> StringSequence;

    struct Question
    {
        string text;
        StringSequence options;
        int correctOption;
    }

    interface Game
    {
        void login(string name);
        void answerQuestion(int questionId, int answer);
        Question getQuestion();
        int getScore();
        bool isOpponentConnected();
    }
}