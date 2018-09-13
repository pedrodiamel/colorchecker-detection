
#include "gtest/gtest.h"
#include "core.h"
#include "checker_detector.h"


struct A
{
	int a = 0;
	A() { }
};

TEST(MCCTest, TestA) {

	A a;
	EXPECT_EQ(0, a.a);

}

int main(int argc, char *argv[])
{
	testing::InitGoogleTest(&argc, argv);
	return RUN_ALL_TESTS();
}