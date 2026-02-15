export default function CustomerDetailLoading() {
  return (
    <div className="min-h-screen bg-[#F4F5F7]">
      {/* Header Skeleton */}
      <header className="border-b border-gray-200 bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-8 py-5">
          <div className="w-48 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
          <div className="w-64 h-4 bg-gray-100 rounded animate-pulse"></div>
        </div>
      </header>

      {/* Main Content Skeleton */}
      <main className="max-w-7xl mx-auto px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Customer Info Skeleton */}
          <div className="lg:col-span-2 space-y-6">
            {/* Customer Header */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="flex items-center gap-6">
                <div className="w-20 h-20 bg-gray-200 rounded-full animate-pulse"></div>
                <div className="flex-1">
                  <div className="w-48 h-8 bg-gray-200 rounded animate-pulse mb-2"></div>
                  <div className="w-32 h-4 bg-gray-100 rounded animate-pulse mb-3"></div>
                  <div className="w-24 h-6 bg-gray-200 rounded-full animate-pulse"></div>
                </div>
              </div>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
                  <div className="w-24 h-4 bg-gray-200 rounded animate-pulse mb-3"></div>
                  <div className="w-32 h-8 bg-gray-200 rounded animate-pulse"></div>
                </div>
              ))}
            </div>

            {/* AI Insights */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-32 h-6 bg-gray-200 rounded animate-pulse mb-4"></div>
              <div className="space-y-2">
                <div className="w-full h-4 bg-gray-100 rounded animate-pulse"></div>
                <div className="w-full h-4 bg-gray-100 rounded animate-pulse"></div>
                <div className="w-3/4 h-4 bg-gray-100 rounded animate-pulse"></div>
              </div>
            </div>

            {/* SHAP Chart */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
            </div>
          </div>

          {/* Right Column - Offer & Actions Skeleton */}
          <div className="space-y-6">
            {/* Recommended Offer */}
            <div className="bg-white rounded-lg border border-gray-200 p-8 shadow-sm">
              <div className="w-40 h-6 bg-gray-200 rounded animate-pulse mb-6"></div>
              <div className="space-y-4">
                <div className="w-full h-6 bg-gray-200 rounded animate-pulse"></div>
                <div className="w-full h-4 bg-gray-100 rounded animate-pulse"></div>
                <div className="w-3/4 h-4 bg-gray-100 rounded animate-pulse"></div>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
              <div className="w-32 h-5 bg-gray-200 rounded animate-pulse mb-4"></div>
              <div className="space-y-2">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="w-full h-10 bg-gray-100 rounded-lg animate-pulse"></div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
